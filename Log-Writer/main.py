import base64
import functions_framework

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


        # Write to firestore here
        print(f"message received by log writer: {data}")

    except Exception as e:
        print(f"Error updating logs in log writer: {e}")
    