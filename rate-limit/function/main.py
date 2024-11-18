'''Rate-Limiting Module Main'''
import base64
import functions_framework
from RateLimiter import rate_limit

# Convert input to batch format
@functions_framework.cloud_event
def process_message(cloud_event):
    try:
        # Process incoming message as a 'batch'
        batch = {
            'client_id': cloud_event.data["message"]["attributes"]["Client_ID"],
            'message': base64.b64decode(cloud_event.data["message"]["data"]).decode('utf-8'),
            'row': cloud_event.data["message"]["attributes"]["Row_Number"],
            'job_id': cloud_event.data["message"]["attributes"]["Job_ID"],
            'user_project_id': cloud_event.data["message"]["attributes"]["User_Project_ID"],
            'user_dataset_id': cloud_event.data["message"]["attributes"]["User_Dataset_ID"],
            'job_length': cloud_event.data["message"]["attributes"]["Job_Length"],
            'output_table_id': cloud_event.data["message"]["attributes"]["Output_Table_ID"],
            'model': cloud_event.data["message"]["attributes"]["Model"],
            'api_key': cloud_event.data["message"]["attributes"]["API_key"]
        }
        print(f"Rate-limiter received message for row {batch['row']} for job {batch['job_id']} from batch processor.") 

        # Process the batch
        rate_limit(batch)

    except Exception as e:
        print(f"Error processing message in rate limiter: {e}") 
        raise