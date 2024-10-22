'''Simple single global token bucket'''
from openai import OpenAI
import redis
import tiktoken
import time

# Initialize Redis connection and bucket info
redis_client = redis.Redis(host='localhost', port=6379, db=0)
GLOBAL_BUCKET_KEY = "global_token_bucket"
tpm = 200000 # 200,000 tpm rate for gpt3.5

# Initialize OpenAI tokenizer
tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")  # Adjust for your model

# OpenAI client
client = OpenAI(api_key="")

################ TOKENIZER ########################
def openai_tokenizer(messages) -> int:
    # Overpredict amnt of tokens needed
    total_tokens = 0

    for message in messages:
        total_tokens += len(tokenizer.encode(message["role"]))
        total_tokens += len(tokenizer.encode(message["content"]))
        total_tokens += 2  # <im_start> and <im_end>

    total_tokens += 2  # For message start/end separators

    # Add large buffer for safety
    buffer = int(0.2 * total_tokens)  
    total_tokens += buffer

    # Add estimated reply size (scaled for longer responses)
    total_tokens += 100  # arbitrary amnt to represent long response

    return total_tokens
    
##################### GLOBAL BUCKET FUNCTIONS ########################
def init_global_bucket():
    # Initialize or reset the global bucket to 200000 tokens
    key_type = redis_client.type(GLOBAL_BUCKET_KEY)
    if key_type != b'hash':
        redis_client.delete(GLOBAL_BUCKET_KEY)
    redis_client.hset(GLOBAL_BUCKET_KEY, "tokens", tpm) 
    redis_client.hset(GLOBAL_BUCKET_KEY, "last_updated", int(time.time()))
    print(f"Global bucket initialized with {tpm} tokens")

def get_tokens_from_global(amount):
    # Withdraw tokens from the global bucket using Redis lock
    with redis_client.lock("global_bucket_lock", blocking_timeout=5):
        # Let sub bucket consume tokens        
        tokens = int(redis_client.hget(GLOBAL_BUCKET_KEY, "tokens") or 0)
        print(f"Accessing global bucket. Currently has {tokens} out of {tpm} tokens")

        if tokens >= amount:
            redis_client.hincrby(GLOBAL_BUCKET_KEY, "tokens", -amount)
            print(f"Consumed {amount} tokens from global bucket. {tokens-amount} tokens remaining.")
            return True  # Allocation succeeded
        else:
            print(f"Failed to consume {amount} tokens from global bucket.")
            return False  # Insufficient tokens

################################ SUB BUCKET FUNCTIONS #####################################
def init_user_subbucket(user_id, tokens_needed):
    user_bucket_key = f"user_bucket:{user_id}"
    bucket_exists = redis_client.exists(user_bucket_key)

    with redis_client.lock(f"{user_bucket_key}_lock", blocking_timeout=5):
        # Check if the user bucket already exists
        if bucket_exists:
            print(f"Altering user {user_id}'s subbucket.")
            max_tokens = int(redis_client.hget(user_bucket_key, "max_tokens") or 0)

            # Calculate new max tokens
            new_max = tokens_needed + max_tokens
            print(f"User {user_id} needs {tokens_needed} more tokens.")

            # Try to withdraw additional tokens from global bucket
            if get_tokens_from_global(new_max):
                redis_client.hset(user_bucket_key, "max_tokens", new_max)
                print(f"Added {tokens_needed} tokens to {user_id}'s sub-bucket. Now has {new_max} maximum tokens.")
                return True
            else:
                print(f"Insufficient global tokens to add {tokens_needed} tokens.")
                return False

        else:
            # If bucket doesn't exist, initialize a new one
            if get_tokens_from_global(tokens_needed):
                current_time = int(time.time())
                redis_client.hset(user_bucket_key, "max_tokens", tokens_needed)
                redis_client.hset(user_bucket_key, "tokens", tokens_needed)
                redis_client.hset(user_bucket_key, "last_updated", current_time)
                print(f"Initialized new sub-bucket for user {user_id} with {tokens_needed} tokens.")
                return True
            else:
                print(f"Failed to initialize sub-bucket for {user_id}. Insufficient global tokens.")
                return False

def get_tokens_from_user(user_id, tokens_needed):
    user_bucket_key = f"user_bucket:{user_id}"

    with redis_client.lock(f"{user_bucket_key}_lock", blocking_timeout=5):
        current_time = int(time.time())
        last_updated = int(redis_client.hget(user_bucket_key, "last_updated") or 0)

        # Refill logic, if a minute has passed, reset to max tokens since tpm reset
        if current_time - last_updated > 60:
            max_tokens = int(redis_client.hget(user_bucket_key, "max_tokens") or 0)
            redis_client.hset(user_bucket_key, "tokens", max_tokens)
            redis_client.hset(user_bucket_key, "last_updated", current_time)
            print(f"Refilled bucket for user {user_id} to {max_tokens} tokens.")
        
        # Consume tokens for job
        tokens = int(redis_client.hget(user_bucket_key, "tokens") or 0)
        if tokens >= tokens_needed:
            redis_client.hincrby(user_bucket_key, "tokens", -tokens_needed)
            print(f"Consumed {tokens_needed} tokens from {user_id}'s sub-bucket.")
            return True
        else:
            print(f"Insufficient tokens in {user_id}'s bucket. Needed: {tokens_needed}, Available: {tokens}.")
            return False

# LLM API call
def call_openai(messages):
    # Make a call to the OpenAI API and track token usage
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        print(f"Actually used {response.usage.total_tokens} tokens") # Print used tokens 
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"OpenAI API call failed: {e}")
        return None

# Batch process
def process(item):
    user_id = item['user_id']
    prompt = item['prompt']
    data = item['data']

    # format for openai
    messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt + data},
            ]
    
    # predict needed tokens
    tokens_needed = openai_tokenizer(messages)
    print(f"Predicting {tokens_needed} tokens needed")

    if not init_user_subbucket(user_id, tokens_needed):
        print("Failed to initialize sub-bucket. Aborting batch.")

    # try to run
    if get_tokens_from_user(user_id, tokens_needed):
        print("Sufficient tokens available, calling OpenAI...")
        # response_content = call_openai(messages)
        # print(f"Response: {response_content}")
    else:
        print("Insufficient tokens in user bucket.")

    
# Simple test

# Initialize global bucket
user_bucket_key = "user_bucket:user123"
if redis_client.exists(user_bucket_key):
    redis_client.delete(user_bucket_key)
init_global_bucket()

# batch data
batch = {
    'user_id': "user123",
    'prompt': "Solve: ",
    'data': "1+1"
}

process(batch)