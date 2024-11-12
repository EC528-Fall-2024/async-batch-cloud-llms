import base64
import functions_framework
from handleGo import handleGo

# Triggered from a message on a Cloud Pub/Sub topic.
@functions_framework.cloud_event
def go(cloud_event):
    try:
        # Get data from Pub/Sub topic
        data = base64.b64decode(cloud_event.data["message"]["data"]).decode('utf-8')
        job_id = cloud_event.data["message"]["attributes"]["Job_ID"]
        client_id = cloud_event.data["message"]["attributes"]["Client_ID"]

        # Print received message and attributes 
        print(f"Received message: {data}") 
        print(f"Job_ID: {job_id}") 
        print(f"Client_ID: {client_id}") 
        
        # database length is hardcoded at the moment
        jobStatus = handleGo(job_id, client_id, 13)
    
    except Exception as e:
        print(f"Error processing message in reverse batch processor: {e}") 
        raise
    
