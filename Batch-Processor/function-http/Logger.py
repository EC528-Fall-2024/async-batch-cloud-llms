from google.cloud import pubsub_v1

microservice = "BatchProcessor"

# send log messages to job orchestrator
def log(message, job_id, client_id, error_type, row):
    project_id = "elated-scope-437703-h9"
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, "Logs")

    message = f"{message}".encode("utf-8")

    # Define attributes as a dictionary
    attributes = {
        "Log_Type": "Error",
        "Microservice": f"{microservice}",
        "Job_ID": f"{job_id}",
        "Client_ID" : f"{client_id}",
        "Row_Number": f"{row}",
        "Num_Rows" : "", # empty since error log
        "Error_Type": f"{error_type}"
    }

    publisher.publish(topic_path, message, **attributes)
    print(f"Sent error log message to job orchestrator.")