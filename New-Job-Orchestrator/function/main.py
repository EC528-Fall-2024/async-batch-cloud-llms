import base64
import functions_framework
from InvokeBatchProcessor import call_batch_processor
from FirestoreWriter import writeJobOrchestratorInformation

# Triggered from a message on a Cloud Pub/Sub topic
@functions_framework.cloud_event
def start_job(cloud_event):
    try:
        # Get data from Pub/Sub topic
        data = base64.b64decode(cloud_event.data["message"]["data"]).decode('utf-8')
        job_id = cloud_event.data["message"]["attributes"]["Job_ID"]
        client_id = cloud_event.data["message"]["attributes"]["Client_ID"]
        project_ID = cloud_event.data["message"]["attributes"]["User_Project_ID"]
        dataset_ID = cloud_event.data["message"]["attributes"]["User_Dataset_ID"]
        input_table_ID = cloud_event.data["message"]["attributes"]["Input_Table_ID"]
        output_table_ID = cloud_event.data["message"]["attributes"]["Output_Table_ID"]
        model = cloud_event.data["message"]["attributes"]["Model"]
        API_key = cloud_event.data["message"]["attributes"]["API_key"]

        # Print received message and attributes 
        print(f"Processing {data} for {client_id}'s job {job_id}")

        # Write metadata to database
        writeJobOrchestratorInformation(job_id, client_id, project_ID, dataset_ID, input_table_ID, output_table_ID, model, API_key)

        # Invoke Batch Processor
        call_batch_processor(job_id, client_id, project_ID, dataset_ID, input_table_ID, output_table_ID, model, API_key)
        
    
    except Exception as e:
        print(f"Error processing incoming job in job orchestrator: {e}") 
        raise
    
