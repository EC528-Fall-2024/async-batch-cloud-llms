'''Update Rows Processed'''
import redis
from RedisClient import redis_client

# Count how many rows processed for a job
def incr_rows(job_id):
    try:
        with redis_client.lock(f"{job_id}_lock"):
            key = str(job_id)

            # Initialize row counter for job if first row
            if not redis_client.exists(key):
                redis_client.hset(key, "num_rows", 0)

            # Increment rows processed counter
            redis_client.hincrby(key, "num_rows", 1)

            # Return status
            rows = int(redis_client.hget(key, "num_rows"))
            return rows
    
    # uncontrollable errors
    except redis.exceptions.RedisError as e:
        print(f"Error accessing Redis for processed rows for job id {job_id}: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error incrementing processed rows for job id {job_id}: {e}")
        return None 