'''Request Limiter Functions'''
import redis
import time
import math
from RedisClient import redis_client, REQUEST_KEY

# Request limiting variables
rpm = 500 # 500 request/min
chunks = 60 # split request limit across minute via chunks
max_requests = math.floor(rpm/chunks) # n requests
request_timer = 60/chunks # t seconds

# Initialize request limiter at start of instance
def init_request_limiter():
    try:
        # Initialize request limiter
        key_type = redis_client.type(REQUEST_KEY)
        if key_type != b'hash':
            redis_client.delete(REQUEST_KEY)
        redis_client.hset(REQUEST_KEY, "request_count", 0) 
        redis_client.hset(REQUEST_KEY, "last_reset", int(time.time()))
        print("Initialized request limiter")
        return True

    # uncontrollable errors
    except redis.exceptions.RedisError as e:
        print(f"Error accessing Redis globally: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error for get_tokens_from_global: {e}")
        return False 

# Update request limiter for every processing request
def incr_request():
    # Approve request under request limiter
    try:
        with redis_client.lock("request_lock"):
            last_updated = int(redis_client.hget(REQUEST_KEY, "last_reset") or 0)
            current_requests = int(redis_client.hget(REQUEST_KEY, "request_count") or 0)

            # If past reset period, reset request count to 0
            if int(time.time()) - last_updated > request_timer:
                redis_client.hset(REQUEST_KEY, "request_count", 0) # reset request count to 0
                redis_client.hset(REQUEST_KEY, "last_reset", int(time.time())) # update last updated time

            # Need to wait till request timer resets if no more requests allowed during this period
            elif current_requests >= max_requests:
                print("Waiting until next request reset period")
                while int(time.time()) - last_updated < request_timer:
                    time.sleep(0.1) # pass time
                redis_client.hset(REQUEST_KEY, "request_count", 0) # reset request count to 0
                redis_client.hset(REQUEST_KEY, "last_reset", int(time.time())) # update last updated time
            
            # Request processed 
            redis_client.hincrby(REQUEST_KEY, "request_count", 1)
            return True
        
    # uncontrollable errors 
    except redis.exceptions.RedisError as e:
        print(f"Error accessing Redis globally: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error for get_tokens_from_global: {e}")
        return False 