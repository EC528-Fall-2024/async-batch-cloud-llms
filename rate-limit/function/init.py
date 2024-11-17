'''Initialize Limiters'''
from RequestLimiter import init_request_limiter
from GlobalBucket import init_global_bucket

# Initialize limiters
def init_limiters():
    if not init_global_bucket():
        print("Failed to initialize global bucket")
        return False
    if not init_request_limiter:
        print("Failed to initialize request limiter")
        return False
    return True