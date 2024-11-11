'''Rate-Limiting Module'''
import openai
import redis
import tiktoken
import time
import requests
import math
import random
from google.cloud import pubsub_v1
import sys
import signal
import threading
import base64
import functions_framework

########################## GENERAL VARIABLES #########################
# Pub/sub topic info for incoming batches
project_id = "elated-scope-437703-h9"
input_topic = "InputData-sub"
output_topic = "OutputData"

# Initialize Redis connection and bucket info
redis_client = redis.Redis(host='localhost', port=6379, db=0)
GLOBAL_BUCKET_KEY = "global_token_bucket"
model = "gpt-3.5-turbo"
role = "You are a helpful assistant."

tpm = 200000 # 200,000 tpm rate for gpt3.5
token_limit = tpm
refill_time = 60 # every minute, tpm resets

# Initialize OpenAI tokenizer
tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")  # Adjust for your model

# OpenAI client
api_key = ""
client = openai.OpenAI(api_key=api_key) 

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
    redis_client.hset(GLOBAL_BUCKET_KEY, "tokens", token_limit) 
    redis_client.hset(GLOBAL_BUCKET_KEY, "last_updated", int(time.time()))
    print(f"Global bucket initialized with {token_limit} tokens") # LOGGING HERE

################################ SUB BUCKET FUNCTIONS #####################################
def get_tokens_from_global(amount, user_id): 
    # Withdraw tokens from the global bucket using Redis lock, we assume amount < token_limit
    try:
        with redis_client.lock("global_bucket_lock"):
            # Let sub bucket consume tokens        
            tokens = int(redis_client.hget(GLOBAL_BUCKET_KEY, "tokens") or 0)

            # wait until tokens in global bucket
            if tokens<amount:
                print(f"{user_id} waiting for tokens from global bucket.") # LOGGING
            while tokens<amount:
                tokens = int(redis_client.hget(GLOBAL_BUCKET_KEY, "tokens") or 0)
                time.sleep(60) # brief sleep between checks

            # take tokens
            redis_client.hincrby(GLOBAL_BUCKET_KEY, "tokens", -amount)
            print(f"{user_id} consumed {amount} tokens from global bucket. Had {tokens} tokens, now {tokens-amount} tokens.") #LOGGING
            return True  # Allocation succeeded
            
    # uncontrollable errors - LOGGING
    except redis.exceptions.RedisError as e:
        print(f"Error accessing Redis globally: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error for get_tokens_from_global: {e}")
        return False 
        
def init_user_subbucket(user_id, tokens_needed):
    # Initialize a user subbucket or update if exists
    user_bucket_key = f"user_bucket:{user_id}"
    try:
        # Try to remove tokens from global before locking user bucket to avoid spin in global bucket while holding lock
        get_tokens_from_global(tokens_needed, user_id)
        
        # Now 'allocate tokens' to bucket
        with redis_client.lock(f"{user_bucket_key}_lock"):
            # Check if the user bucket already exists
            bucket_exists = redis_client.exists(user_bucket_key)
            if bucket_exists:
                # Calculate new max tokens
                max_tokens = int(redis_client.hget(user_bucket_key, "max_tokens") or 0)
                new_max = tokens_needed + max_tokens

                # 'Allocate tokens'
                tokens = int(redis_client.hget(user_bucket_key, "tokens") or 0)
                tokens = tokens + tokens_needed # add to curr tokens as well
                redis_client.hset(user_bucket_key, "tokens", tokens)
                redis_client.hset(user_bucket_key, "max_tokens", new_max)
                print(f"Added {tokens_needed} tokens to {user_id}'s sub-bucket. Now has {new_max} maximum tokens.") # LOGGING
                return True

            # If bucket doesn't exist, initialize a new one
            else:
                # 'Allocate tokens'
                current_time = int(time.time())
                redis_client.hset(user_bucket_key, "max_tokens", tokens_needed)
                redis_client.hset(user_bucket_key, "max_tokens_at_update", tokens_needed)
                redis_client.hset(user_bucket_key, "tokens", tokens_needed)
                redis_client.hset(user_bucket_key, "last_updated", current_time)
                print(f"Initialized new sub-bucket for user {user_id} with {tokens_needed} tokens.") # LOGGING
                return True
                
    # uncontrollable errors - LOGGING
    except redis.exceptions.RedisError as e:
        print(f"Error accessing Redis for user {user_id}: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error in init_user_subbucket for user {user_id}: {e}")
        return False

def get_tokens_from_user(user_id, tokens_needed):
    user_bucket_key = f"user_bucket:{user_id}"
    try:
        with redis_client.lock(f"{user_bucket_key}_lock"):
            current_time = int(time.time())
            last_updated = int(redis_client.hget(user_bucket_key, "last_updated") or 0)

            # Refill logic, if a refill_time has passed, reset to max tokens
            if current_time - last_updated > refill_time:
                max_tokens = int(redis_client.hget(user_bucket_key, "max_tokens") or 0)
                old_max_tokens = int(redis_client.hget(user_bucket_key, "max_tokens_at_update") or 0)
                redis_client.hset(user_bucket_key, "tokens", old_max_tokens)
                redis_client.hset(user_bucket_key, "max_tokens_at_update", max_tokens)
                redis_client.hset(user_bucket_key, "last_updated", current_time)
                print(f"Refilled bucket for user {user_id} to {max_tokens} tokens.") # LOGGING
            
            # Check tokens in user bucket
            tokens = int(redis_client.hget(user_bucket_key, "tokens") or 0)

            # Spin until enough tokens in user bucket --> new implementation guarantees enough tokens in user bucket
            # print(f"Waiting until enough tokens in {user_id} token bucket") 
            # while(tokens<tokens_needed):
            #     tokens = int(redis_client.hget(user_bucket_key, "tokens") or 0)

            # Consume tokens
            redis_client.hincrby(user_bucket_key, "tokens", -tokens_needed)
            print(f"Consumed {tokens_needed} tokens from {user_id}'s sub-bucket.") # LOGGING
            return True
            
    # uncontrollable errors - LOGGING
    except redis.exceptions.RedisError as e:
        print(f"Error acessing Redis for user {user_id}: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error in get_tokens_from_user for user {user_id}: {e}")
        return False

def ret_used_tokens(tokens):
    # wait minute
    time.sleep(1)

    # return used tokens to global bucket
    with redis_client.lock("global_increase"):
        redis_client.hincrby(GLOBAL_BUCKET_KEY, "tokens", tokens)

    # log status
    global_tokens = int(redis_client.hget(GLOBAL_BUCKET_KEY, "tokens") or 0)
    print(f"Global bucket increased to {global_tokens} tokens.") # LOGGING

def shrink_user_bucket(user_id, tokens_used, actual_used):
    user_bucket_key = f"user_bucket:{user_id}"
    try:
        with redis_client.lock(f"{user_bucket_key}_lock"):
            # Get user bucket state
            max_tokens = int(redis_client.hget(user_bucket_key, "max_tokens") or 0)

            # Update user max tokens
            new_max = max_tokens - tokens_used
            if new_max != 0:
                redis_client.hset(user_bucket_key, "max_tokens", new_max)
                print(f"Shrunk {user_id}'s bucket by {tokens_used} tokens. New max: {new_max}") # LOGGING
            else:
                redis_client.delete(user_bucket_key)
                print(f"All batches for user {user_id} complete, destroyed bucket.") # LOGGING

    # uncontrollable errors - LOGGING
    except redis.exceptions.RedisError as e:
        print(f"Error accessing Redis for shrinking buckets for user {user_id}: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error in shrinking the buckets for user {user_id}: {e}")
        return False

    # Return tokens to global bucket 
    try:
        # Return unused tokens immediately
        if(tokens_used-actual_used>0):
            with redis_client.lock("global_increase"):
                redis_client.hincrby(GLOBAL_BUCKET_KEY, "tokens", max(tokens_used-actual_used,0))
                # log status
                global_tokens = int(redis_client.hget(GLOBAL_BUCKET_KEY, "tokens") or 0)
                print(f"Global bucket increased to {global_tokens} tokens.") # LOGGING

        # Return used tokens a minute later
        used = min(actual_used, tokens_used)
        if used > 0:
            thread = threading.Thread(target=ret_used_tokens, args=(used,)).start()
    
    # uncontrollable errors - LOGGING
    except redis.exceptions.RedisError as e:
        print(f"Error returning tokens back into bucket for user {user_id}: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error in returning buckets for user {user_id}: {e}")
        return False

############################## LLM API call #############################
def call_openai(messages, user_id, tokens_needed, api_key, counter = 1, delay = 5):
    # Assume this job needs to be dropped
    if(delay>120):
        print("Unexpected error in call_openai")
        return None
    # Make a call to the OpenAI API and track token usage
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages
        )
        actual = response.usage.total_tokens
        return response.choices[0].message.content.strip(), actual, counter
    
    # If openai_api call fails, assume incorrect prediction of tokens
    except openai.RateLimitError as e: 
        print(f"OpenAI API rate limit has been reached, increasing {user_id}'s token bucket before retrying...") # LOGGING
        
        # If rate limit error, add tokens to the user bucket, caps at token_limit
        tokens_needed = min(token_limit-tokens_needed, tokens_needed)
        if not init_user_subbucket(user_id, tokens_needed):
            print("Failed to update sub-bucket. Aborting batch.")
            return
        if delay > 5: # no delay initially
            print(f"Trying to run request again for {user_id} after {delay} seconds") # LOGGING
            time.sleep(delay)

        # double delay on each call - exponential backoff
        # note the size of bucket expanding via counter (size = counter*tokens_needed)
        return call_openai(messages, user_id, tokens_needed, api_key, counter+1, delay*2)
    
    # If want to have a timeout:
    # except requests.exceptions.Timeout as e:
    #     print(f"OpenAI API call timed out after {timeout} seconds: {e}")
    #     return None

    # uncontrollable errors - LOGGING HERE
    except Exception as e:
        if isinstance(e, openai.APIConnectionError):
            error_message = f"OpenAI API Connection error: {e}"
        elif isinstance(e, openai.APITimeoutError):
            error_message = f"OpenAI API Timeout error:{e}"
        elif isinstance(e, openai.AuthenticationError):
            error_message = f"OpenAI Authentication error:{e}"
        elif isinstance(e, openai.BadRequestError):
            error_message = f"OpenAI Bad Request error:{e}"
        elif isinstance(e, openai.ConflictError):
            error_message = f"OpenAI Conflict error:{e}"
        elif isinstance(e, openai.InternalServerError):
            error_message = f"OpenAI Internal Server error:{e}"
        elif isinstance(e, openai.NotFoundError):
            error_message = f"OpenAI Not Found error:{e}"
        elif isinstance(e, openai.PermissionDeniedError):
            error_message = f"OpenAI Permission Denied error:{e}"
        elif isinstance(e, openai.UnprocessableEntityError):
            error_message = f"OpenAI Unprocessed Entity error: {e}"
        else:
            error_message = f"Unexpected error in call_openai: {e}"
        print(error_message) # LOGGING
        return None, tokens_needed, counter

######################## PUBLISH TO REVERSE BATCH PROESSOR ###############################
def send_response(client_id, job_id, row, response):
    publisher = pubsub_v1.PublisherClient()
    publisher_path = publisher.topic_path(project_id, output_topic)

    # Response must be a bytestring
    message = response.encode("utf-8")
    
    # Define attributes as a dictionary
    attributes = {
        "Job_ID": f"{job_id}",
        "Client_ID": f"{client_id}",
        "Row_Number": f"{row}"
    }

    # Send out response via pub/sub
    future = publisher.publish(publisher_path, message, **attributes)
    future.result()
    print("Sent response to reverse batch processor") # LOGGING

# Batch process
def process(batch):
    user_id = batch['client_id'] 
    message = batch['message']
    job_id = batch['job_id']
    row = batch['row']

    # format for openai
    messages=[
                {"role": "system", "content": role},
                {"role": "user", "content": message},
            ]
    
    # predict needed tokens
    tokens_needed = openai_tokenizer(messages)
    print(f"Predicting {tokens_needed} tokens needed")

    if not init_user_subbucket(user_id, tokens_needed):
        print("Failed to initialize sub-bucket. Aborting batch.")
        return

    # try to run
    if get_tokens_from_user(user_id, tokens_needed):
        # Call LLM API
        print("Attempting to call OpenAI...") # LOGGING
        # response_content, actual_tokens, counter = "fake_response", tokens_needed, 1 # for testing
        # time.sleep(0.1) # simulate delay for testing
        response_content, actual_tokens, counter = call_openai(messages, user_id, tokens_needed, api_key)
        if response_content is None:
            print("OpenAI API call failed, sending back tokens & aborting")
            shrink_user_bucket(user_id,min(tokens_needed*counter,token_limit), actual_tokens)
            return
        print(f"Received Response: {response_content}") # LOGGING

        # Response Logic
        send_response(user_id, job_id, row, response_content)

        # Shrink user bucket accordingly since job complete
        shrink_user_bucket(user_id,min(tokens_needed*counter,token_limit), actual_tokens)
    else:
        print("Issue with accessing tokens from user bucket. Aborting batch")

############################### MAIN ###################################
# Initialize local bucket & start Pub/Sub trigger handler
init_global_bucket()

@functions_framework.cloud_event
def pubsub_event(cloud_event):
    # Get data from Pub/Sub topic
    message = base64.b64decode(cloud_event.data["message"]["data"]).decode('utf-8')
    job_id = cloud_event.data["message"]["attributes"]["Job_ID"]
    client_id = cloud_event.data["message"]["attributes"]["Client_ID"]
    row_number = cloud_event.data["message"]["attributes"]["Row_Number"]

    batch = {
        'client_id': client_id,
        'message': message,
        'row': row_number,
        'job_id': job_id
    }

    process(batch)
    