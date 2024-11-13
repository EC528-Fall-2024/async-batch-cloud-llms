import base64
import functions_framework
from BigQueryWriter import write_response

# Triggered from a message on a Cloud Pub/Sub topic.
@functions_framework.cloud_event
def reverse(cloud_event):
    try:
        # Get data from Pub/Sub topic
        data = base64.b64decode(cloud_event.data["message"]["data"]).decode('utf-8')
        job_id = cloud_event.data["message"]["attributes"]["Job_ID"]
        client_id = cloud_event.data["message"]["attributes"]["Client_ID"]
        row_number = cloud_event.data["message"]["attributes"]["Row_Number"]

        # Print received message and attributes 
        print(f"Received message: {data}, Job_ID: {job_id}, Client_ID: {client_id}, Row_Number: {row_number}") 

        # Write the message to a database 
        write_response(data, row_number, job_id, client_id)
    
    except Exception as e:
        print(f"Error processing message in reverse batch processor: {e}") 
        raise
    
