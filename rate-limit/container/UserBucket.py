'''User Bucket Functions'''
import redis
import threading
import time
from GlobalBucket import get_tokens_from_global
from RedisClient import redis_client, GLOBAL_BUCKET_KEY

# Initialize/Update a user bucket
def update_user_bucket(user_id, tokens_needed):
    # Initialize a user subbucket or update if exists
    user_bucket_key = f"user_bucket:{user_id}"
    try:
        # Try to remove tokens from global before locking user bucket to avoid spin in global bucket while holding lock
        get_tokens_from_global(tokens_needed, user_id)
        
        # Now allocate tokens to bucket
        with redis_client.lock(f"{user_bucket_key}_lock"):
            # Check if the user bucket already exists
            bucket_exists = redis_client.exists(user_bucket_key)
            if bucket_exists:
                # Calculate new max tokens
                max_tokens = int(redis_client.hget(user_bucket_key, "max_tokens") or 0)
                new_max = tokens_needed + max_tokens

                # Allocate tokens
                tokens = int(redis_client.hget(user_bucket_key, "tokens") or 0)
                tokens = tokens + tokens_needed # add to curr tokens as well
                redis_client.hset(user_bucket_key, "tokens", tokens)
                redis_client.hset(user_bucket_key, "max_tokens", new_max)
                print(f"Added {tokens_needed} tokens to {user_id}'s sub-bucket. Now has {new_max} maximum tokens.") 
                return True

            # If bucket doesn't exist, initialize a new one
            else:
                # Allocate tokens
                current_time = int(time.time())
                redis_client.hset(user_bucket_key, "max_tokens", tokens_needed)
                redis_client.hset(user_bucket_key, "max_tokens_at_update", tokens_needed)
                redis_client.hset(user_bucket_key, "tokens", tokens_needed)
                redis_client.hset(user_bucket_key, "last_updated", current_time)
                print(f"Initialized new sub-bucket for user {user_id} with {tokens_needed} tokens.") 
                return True
                
    # uncontrollable errors 
    except redis.exceptions.RedisError as e:
        print(f"Error accessing Redis for user {user_id}: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error in update_user_subbucket for user {user_id}: {e}")
        return False

# Job removes tokens from user bucket
def get_tokens_from_user(user_id, tokens_needed, refill_time):
    user_bucket_key = f"user_bucket:{user_id}"
    try:
        with redis_client.lock(f"{user_bucket_key}_lock"):
            current_time = int(time.time())
            last_updated = int(redis_client.hget(user_bucket_key, "last_updated") or 0)

            # Refill logic, if refill_time has passed, reset to max tokens
            if current_time - last_updated > refill_time:
                max_tokens = int(redis_client.hget(user_bucket_key, "max_tokens") or 0)
                old_max_tokens = int(redis_client.hget(user_bucket_key, "max_tokens_at_update") or 0)
                redis_client.hset(user_bucket_key, "tokens", old_max_tokens)
                redis_client.hset(user_bucket_key, "max_tokens_at_update", max_tokens)
                redis_client.hset(user_bucket_key, "last_updated", current_time)
                print(f"Refilled bucket for user {user_id} to {max_tokens} tokens.")

            # Consume tokens
            redis_client.hincrby(user_bucket_key, "tokens", -tokens_needed)
            print(f"Consumed {tokens_needed} tokens from {user_id}'s sub-bucket.") 
            return True
            
    # uncontrollable errors 
    except redis.exceptions.RedisError as e:
        print(f"Error acessing Redis for user {user_id}: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error in get_tokens_from_user for user {user_id}: {e}")
        return False
    
# Delayed return of tokens to bucket
def ret_used_tokens(tokens, refill_time):
    # Wait refill_time
    time.sleep(refill_time)

    # Return used tokens to global bucket
    with redis_client.lock("global_increase"):
        redis_client.hincrby(GLOBAL_BUCKET_KEY, "tokens", tokens)

    # Logging
    global_tokens = int(redis_client.hget(GLOBAL_BUCKET_KEY, "tokens") or 0)
    print(f"Global bucket increased to {global_tokens} tokens.") 

# Attempt to shrink/destroy the user bucket
def shrink_user_bucket(user_id, tokens_used, actual_used, refill_time):
    user_bucket_key = f"user_bucket:{user_id}"
    try:
        with redis_client.lock(f"{user_bucket_key}_lock"):
            max_tokens = int(redis_client.hget(user_bucket_key, "max_tokens") or 0)

            # Update user max tokens
            new_max = max_tokens - tokens_used
            if new_max != 0:
                redis_client.hset(user_bucket_key, "max_tokens", new_max)
                print(f"Shrunk {user_id}'s bucket by {tokens_used} tokens. New max: {new_max}") 
            else:
                redis_client.delete(user_bucket_key)
                print(f"All batches for user {user_id} complete, destroyed bucket.") 

    # uncontrollable errors 
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
                print(f"Global bucket increased to {global_tokens} tokens.") 

        # Return used tokens a minute later
        used = min(actual_used, tokens_used)
        if used > 0:
            thread = threading.Thread(target=ret_used_tokens, args=(used,refill_time,)).start()
    
    # uncontrollable errors
    except redis.exceptions.RedisError as e:
        print(f"Error returning tokens back into bucket for user {user_id}: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error in returning buckets for user {user_id}: {e}")
        return False