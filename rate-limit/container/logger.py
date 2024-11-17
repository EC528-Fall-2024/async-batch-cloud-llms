'''Send Mesages to Job Orchestrator'''
from google.cloud import pubsub_v1

project_id = "elated-scope-437703-h9"
microservice = "RateLimiter"
error_topic = "ErrorLogs"
progress_topic = "ProgressLogs"

# send log messages to job orchestrator
def error_message(message, job_id, client_id, error_type, row):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, error_topic)

    message = f"{message}".encode("utf-8")

    # Define attributes as a dictionary
    attributes = {
        "Job_ID": f"{job_id}",
        "Client_ID": f"{client_id}",
        "Microservice:": f"{microservice}",
        "Error_Type": f"{error_type}",
        "Row_Number": f"{row}"
    }

    publisher.publish(topic_path, message, **attributes)
    print(f"Sent {error_topic} message to job orchestrator.")

def progress_message(message, job_id, client_id, num_rows):
    project_id = "elated-scope-437703-h9"
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, progress_topic)

    message = f"{message}".encode("utf-8")

    # Define attributes as a dictionary
    attributes = {
        "Job_ID": f"{job_id}",
        "Client_ID": f"{client_id}",
        "Num_Rows": f"{num_rows}"
    }

    publisher.publish(topic_path, message, **attributes)
    print(f"Sent {progress_topic} message to job orchestrator.")