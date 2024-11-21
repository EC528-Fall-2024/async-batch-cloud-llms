'''Send Mesages to Job Orchestrator'''
from google.cloud import pubsub_v1

project_id = "elated-scope-437703-h9"
microservice = "RateLimiter"
topic = "Logs"

# send log messages to job orchestrator
def error_message(message, job_id, client_id, error_type, row):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic)

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
    print(f"Sent error message to job orchestrator.")

def progress_message(message, job_id, client_id, rows_processed, job_length):
    project_id = "elated-scope-437703-h9"
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic)

    message = f"{message}".encode("utf-8")

    # Define attributes as a dictionary
    attributes = {
        "Log_Type": "Progress",
        "Microservice": f"{microservice}",
        "Job_ID": f"{job_id}",
        "Client_ID" : f"{client_id}",
        "Row_Number": f"{rows_processed}", # processed rows instead of actual row since progress log
        "Num_Rows" : f"{job_length}",
        "Error_Type": "" # empty since progress log
    }

    publisher.publish(topic_path, message, **attributes)
    print(f"Sent progress message to job orchestrator.")