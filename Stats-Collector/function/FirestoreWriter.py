from google.cloud import firestore
import redis

# set up redis_client
redis_client = redis.Redis(host='10.84.53.171', port=6379, db=0)

# increment rows completed in firestore
def StatsWriter(Job_ID, Client_ID, Row):
    try:
        # unique redis key for each row's stats
        key = f"{Client_ID}_{Job_ID}_{Row}"
        
        # Get vars
        start = float(redis_client.hget(key, "start"))
        in_llm = float(redis_client.hget(key, "in_llm"))
        out_llm = float(redis_client.hget(key, "out_llm"))
        end = float(redis_client.hget(key, "end"))

        # Calculate metrics
        total_time = end - start
        time_before_llm = in_llm - start
        time_in_llm = out_llm - in_llm
        time_after_llm = end - out_llm

        # Use redis lock for updating firestore
        with redis_client.lock(f"{Client_ID}_{Job_ID}_stats_lock"):
            db = firestore.Client()
            doc_ref = db.collection("Clients").document(Client_ID).collection("Jobs").document("Job "+ Job_ID).collection("Job Data").document("Stats")
            
            # get current state
            doc = doc_ref.get()

            # Read current stats and update running averages
            if doc.exists:
                # old stats
                data = doc.to_dict()
                avg_time = data.get('average_time')
                avg_before = data.get('average_time_before_llm')
                avg_in = data.get('average_time_in_llm')
                avg_after = data.get('average_time_after_llm')
                running_rows = data.get('running_rows')

                # new stats
                new_rows = running_rows + 1
                new_avg = ((avg_time*running_rows)+total_time)/(new_rows)
                new_before = ((avg_before*running_rows)+time_before_llm)/(new_rows)
                new_in = ((avg_in*running_rows)+time_in_llm)/(new_rows)
                new_after = ((avg_after*running_rows)+time_after_llm)/(new_rows)

                # write new stats to firestore
                doc_ref.set({
                    "average_time": new_avg,
                    "average_time_before_llm": new_before,
                    "average_time_after_llm": new_in,
                    "average_time_in_llm": new_after,
                    "running_rows": new_rows
                })

            # Create doc with first rows stats 
            else:
                doc_ref.set({
                    "average_time": total_time,
                    "average_time_before_llm": time_before_llm,
                    "average_time_after_llm": time_after_llm,
                    "average_time_in_llm": time_in_llm,
                    "running_rows": 1
                })
        
        print(f"Updated running average times of job {Job_ID}")

        # delete redis key
        redis_client.delete(key)

    except Exception as e:
        print(f"Unexpected error calculating metrics/sending stats to Firestore: {e}")

def end_time(Job_ID, Client_ID):
    try:
        # Use redis lock for updating firestore
        with redis_client.lock(f"{Client_ID}_{Job_ID}_info_lock"):
            db = firestore.Client()
            doc_ref = db.collection("Clients").document(Client_ID).collection("Jobs").document("Job "+ Job_ID).collection("Job Data").document("Orchestrator Information")
            doc_ref.update({
                "End_Time": firestore.SERVER_TIMESTAMP
            })
            print(f"Updated end time in metadata in Firestore since all rows processed for job {Job_ID}")

    except Exception as e:
        print(f"Unexpected error updating end time for job {Job_ID} in Firestore: {e}")

def write_llm_cost(Job_ID, Client_ID, llm_cost):
    try:
        # Use redis lock for updating firestore
        with redis_client.lock(f"{Client_ID}_{Job_ID}_info_lock"):
            db = firestore.Client()
            doc_ref = db.collection("Clients").document(Client_ID).collection("Jobs").document("Job "+ Job_ID).collection("Job Data").document("Orchestrator Information")
            doc = doc_ref.get() # get current state
            data = doc.to_dict() # get variables

            # Write the llm_cost if it doesnt exist
            if data.get("LLM_Cost") is None:
                doc_ref.update({
                    "LLM_Cost": str(llm_cost)
                })
            
            # Add to current llm_cost otherwise
            else:
                data = doc.to_dict()
                curr_cost = data.get("LLM_Cost")
                llm_cost = float(curr_cost) + llm_cost
                doc_ref.update({
                    "LLM_Cost": str(llm_cost)
                })
            
            print(f"Successfully updated LLM cost for job {Job_ID} in Firestore")

    except Exception as e:
        print(f"Error updating LLM Cost for job {Job_ID} in Firestore: {e}")
