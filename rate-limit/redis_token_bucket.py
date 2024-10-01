import time
import redis
from requests.exceptions import HTTPError

# Token Bucket Implementation w Redis
class RedisTokenBucket:
    def __init__(self, redis_client, bucket_key):
        self.redis_client = redis_client
        self.bucket_key = bucket_key

        # Initialize bucket with 0 tokens
        self.redis_client.hmset(bucket_key, {"tokens": 0, "rate_limit_reset": 0})

    def refill(self, llm_tokens_remaining, llm_rate_limit_reset):
        # Get Redis values
        rate_limit_reset_time = float(self.redis_client.hget(self.bucket_key, "rate_limit_reset"))

        if time.time() >= rate_limit_reset_time:
            # Use LLM response data to reset the token bucket
            self.redis_client.hmset(self.bucket_key, {
                "tokens": llm_tokens_remaining, 
                "last_refill": time.time(), 
                "rate_limit_reset": time.time() + llm_rate_limit_reset
            })
            print(f"Rate limit reset period hit. Refilled bucket to {llm_tokens_remaining} tokens")

    def consume(self, num_tokens):
        tokens = float(self.redis_client.hget(self.bucket_key, "tokens"))

        if tokens >= num_tokens:
            # consume token & update shared bucket
            self.redis_client.hincrbyfloat(self.bucket_key, "tokens", -num_tokens)
            return tokens-num_tokens
        return False

# Simulate LLM API
def call_llm_api():
    # Simulate LLM response w headers
    # play around with below variables to see different error handling scenarios
    response = {
        'RateLimit-Remaining': 5, # random remaining tokens for simulation
        'RateLimit-Reset': 10  # time b4 rate limit resets
    }

    # Simulate possible errors
    if response['RateLimit-Remaining'] == 0:
        raise HTTPError("429 Too Many Requests")

    return response

# Error Handling for Rate Limiting
def handle_rate_limit_error(reset_time):
    print(f"Rate limit hit. Waiting for {reset_time} seconds before retrying...")
    time.sleep(reset_time)

# Test Token Bucket with Redis & LLM API Simulation
def process_requests(token_bucket):
    for i in range(10):
        # wait till request goes through
        while(1):
            print(f"Processing request {i+1}...")
            try:
                # Simulate calling LLM API
                api_response = call_llm_api()

                # Give refill logic LLM info
                token_bucket.refill(api_response['RateLimit-Remaining'], api_response['RateLimit-Reset'])

                tokens_consumed = token_bucket.consume(1) # assume each request needs 1 token
                if tokens_consumed:
                    print(f"Token consumed. Remaining tokens in bucket: {tokens_consumed}\n")
                    break
                else:
                    print("No tokens available. Waiting...")
                    handle_rate_limit_error(api_response['RateLimit-Reset'])

            except HTTPError as e:
                print(f'Error: {e}')
                handle_rate_limit_error(5)  # exponential backoff standin

        time.sleep(3)  # Delay to simulate time between requests


# redis setup
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# init redis token bucket
bucket = RedisTokenBucket(redis_client, 'token_bucket')

# simulate request handling
process_requests(bucket)
