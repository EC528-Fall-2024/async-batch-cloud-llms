'''Setup Redis Client'''
import redis

# Initialize Redis connection 
redis_client = redis.Redis(host='localhost', port=6379, db=0)
GLOBAL_BUCKET_KEY = "global_token_bucket"
REQUEST_KEY = "request_limiter"