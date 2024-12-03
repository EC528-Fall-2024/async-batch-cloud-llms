import base64
import functions_framework
import redis
from FirestoreWriter import StatsWriter, end_time, write_llm_cost

# set up redis_client
redis_client = redis.Redis(host='10.84.53.171', port=6379, db=0)

@functions_framework.cloud_event
def update(cloud_event):
    try:
        # Get time data from Pub/Sub topic
        service = base64.b64decode(cloud_event.data["message"]["data"]).decode('utf-8') # Microservice
        job_id = cloud_event.data["message"]["attributes"]["Job_ID"]
        client_id = cloud_event.data["message"]["attributes"]["Client_ID"]
        row = cloud_event.data["message"]["attributes"]["Row"]
        start = cloud_event.data["message"]["attributes"]["Start"]
        in_llm = cloud_event.data["message"]["attributes"]["In_LLM"]
        out_llm = cloud_event.data["message"]["attributes"]["Out_LLM"]
        end = cloud_event.data["message"]["attributes"]["End"]

        # unique redis key for each row's stats
        key = f"{client_id}_{job_id}_{row}"

        if service == "BatchProcessor":
            redis_client.hset(key, "start", start) 
            print(f"Updated start time of job {job_id}'s row {row}")
        
        elif service == "RateLimiter": 
            # standard metric updates
            redis_client.hset(key, "in_llm", in_llm) 
            redis_client.hset(key, "out_llm", out_llm) 
            print(f"Updated llm times of job {job_id}'s row {row}")

            # llm cost update
            llm_cost = float(cloud_event.data["message"]["attributes"]["LLM_Cost"])
            write_llm_cost(job_id, client_id, llm_cost)

        elif service == "ReverseBatchProcessor":
            # get final flag
            final_flag = bool(int(cloud_event.data["message"]["attributes"]["Final_Row_Flag"]))
            if(final_flag):
                # write the final end time to firestore
                end_time(job_id, client_id)
                
            # deal with standard metric updates
            redis_client.hset(key, "end", end) 
            print(f"Updated end time of job {job_id}'s row {row}")
            StatsWriter(job_id, client_id, row)


    except Exception as e:
        print(f"Error updating/calculating stats in stats collector: {e}")