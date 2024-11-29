import base64
import functions_framework
from datetime import datetime
from FirestoreWriter import logProgressWriter, rowErrorWriter

@functions_framework.cloud_event
def log(cloud_event):
    try:
        # Get data from Pub/Sub topic
        data = base64.b64decode(cloud_event.data["message"]["data"]).decode('utf-8')
        log_type = cloud_event.data["message"]["attributes"]["Log_Type"]
        microservice = cloud_event.data["message"]["attributes"]["Microservice"]
        job_id = cloud_event.data["message"]["attributes"]["Job_ID"]
        client_id = cloud_event.data["message"]["attributes"]["Client_ID"]
        row = cloud_event.data["message"]["attributes"]["Row_Number"]
        num_rows = cloud_event.data["message"]["attributes"]["Num_Rows"] # empty if error
        error_type = cloud_event.data["message"]["attributes"]["Error_Type"] # empty if progress

        print(f"{log_type} message from {microservice} received by log writer: {data}")

        # Handle errors here
        if log_type == "Error":
            if error_type == "RowDropped":
                rowErrorWriter(job_id, client_id, int(row), f"Error from {microservice} for row {row} at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}: {data}")
                

        # Write to firebase here
        elif log_type == "Progress":
            logProgressWriter(str(job_id), client_id, int(row), int(num_rows))

    except Exception as e:
        print(f"Error updating logs in log writer: {e}")