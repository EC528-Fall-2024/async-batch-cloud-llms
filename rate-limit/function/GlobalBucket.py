'''Global Bucket Functions'''
import redis
import time
import math
from RedisClient import redis_client, GLOBAL_BUCKET_KEY

# Initialize global bucket
TPM = 200000
TPS = math.ceil(TPM/60)

def init_global_bucket(token_limit = TPM):
    try:
        # Initialize or reset the global bucket to token_limit tokens
        key_type = redis_client.type(GLOBAL_BUCKET_KEY)
        if key_type != b'hash':
            redis_client.delete(GLOBAL_BUCKET_KEY)
        redis_client.hset(GLOBAL_BUCKET_KEY, "tokens", token_limit) 
        redis_client.hset(GLOBAL_BUCKET_KEY, "last_updated", int(time.time()))
        print(f"Global bucket initialized with {token_limit} tokens") 
        return True

    # uncontrollable errors
    except redis.exceptions.RedisError as e:
        print(f"Error accessing Redis globally: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error for init_global_bucket: {e}")
        return False 

# User bucket trying to get tokens from global bucket
def get_tokens_from_global(amount, user_id): 
    # Withdraw tokens from the global bucket using Redis lock
    try:
        with redis_client.lock("global_bucket_lock"):
            # Let sub bucket consume tokens        
            tokens = int(redis_client.hget(GLOBAL_BUCKET_KEY, "tokens") or 0)

            # Wait until tokens in global bucket
            if tokens<amount:
                print(f"{user_id} waiting for tokens from global bucket.") 
                while tokens<amount:
                    last_updated = redis_client.hget(GLOBAL_BUCKET_KEY, "last_updated")
                    time_elapsed = int(time.time()) - int(last_updated)
                    if time_elapsed >= 1:
                        with redis_client.lock("global_increase"):
                            increase_amount = min(TPS*time_elapsed, TPM-tokens)
                            redis_client.hincrby(GLOBAL_BUCKET_KEY, "tokens", increase_amount)
                            redis_client.hset(GLOBAL_BUCKET_KEY, "last_updated", int(time.time()))
                    tokens = int(redis_client.hget(GLOBAL_BUCKET_KEY, "tokens") or 0)
                    time.sleep(0.1) # brief sleep between checks
        
            with redis_client.lock("global_increase"):
                # Take tokens
                redis_client.hincrby(GLOBAL_BUCKET_KEY, "tokens", -amount)
                print(f"{user_id} consumed {amount} tokens from global bucket. Had {tokens} tokens, now {tokens-amount} tokens.")
                return True  # Allocation succeeded
            
    # uncontrollable errors
    except redis.exceptions.RedisError as e:
        print(f"Error accessing Redis globally: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error for get_tokens_from_global: {e}")
        return False 