import base64
import functions_framework
import time
from BigQueryWriter import insert_rows
from performance import incrementReverseBatchProcessor, decrementQueue2
from Logger import send_metrics

# Triggered from a message on a Cloud Pub/Sub topic.
@functions_framework.cloud_event
def reverse(cloud_event):
    try:
        # Get data from Pub/Sub topic
        data = base64.b64decode(cloud_event.data["message"]["data"]).decode('utf-8')
        job_id = cloud_event.data["message"]["attributes"]["Job_ID"]
        client_id = cloud_event.data["message"]["attributes"]["Client_ID"]
        row_number = cloud_event.data["message"]["attributes"]["Row_Number"]
        project_ID = cloud_event.data["message"]["attributes"]["User_Project_ID"]
        dataset_ID = cloud_event.data["message"]["attributes"]["User_Dataset_ID"]
        table_ID = cloud_event.data["message"]["attributes"]["Output_Table_ID"]
        final_row = cloud_event.data["message"]["attributes"]["Final_Row_Flag"]
        

        # Print received message and attributes 
        print(f"Received message: {data}, Job_ID: {job_id}, Client_ID: {client_id}, Row_Number: {row_number}") 

        # Start time metric calculations in stats collector by marking end time
        send_metrics(client_id, job_id, row_number, time.time(), final_row)

        # Write the message to a database 
        insert_rows(response=data, row=row_number, job_id=job_id, client_id=client_id, project_id=project_ID, dataset_id=dataset_ID, table_id=table_ID)
        
        # Send Performance metrics 
        # try:
        #     incrementReverseBatchProcessor(job_id)
        #     decrementQueue2(job_id)
        # except Exception as e:
        #     print(f"Error updating performance metrics: {e}...")
    
    except Exception as e:
        print(f"Error processing message in reverse batch processor: {e}") 
        raise
    
