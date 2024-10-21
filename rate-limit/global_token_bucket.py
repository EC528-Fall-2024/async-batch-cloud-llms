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
    with redis_client.lock("global_bucket_lock", blocking_timeout=5) as lock:
        # Reset global bucket tokens if minute passed
        current_time = int(time.time())
        last_updated = int(redis_client.hget(GLOBAL_BUCKET_KEY, "last_updated") or 0)
        if current_time - last_updated > 60: 
            print(f"More than one minute passed. Resetting tokens to {tpm}")
            redis_client.hset(GLOBAL_BUCKET_KEY, "tokens", 200000)
            redis_client.hset(GLOBAL_BUCKET_KEY, "last_updated", current_time)

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



# Simple test

# Initialize global bucket
init_global_bucket()

# prompt/data
prompt = "Solve: "
data = "1+1"

# format for openai
messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt + data},
        ]

# predict needed tokens
tokens_needed = openai_tokenizer(messages)
print(f"Predicting {tokens_needed} tokens needed")

# try to run
if get_tokens_from_global(tokens_needed):
    print("Sufficient tokens available, calling OpenAI...")
    response_content = call_openai(messages)
    print(f"Response: {response_content}")
else:
    print("Insufficient tokens in global bucket.")