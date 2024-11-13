from google.cloud import pubsub_v1

microservice = "ReverseBatchProcessor"

# send log messages to job orchestrator
def error_message(message, job_id, client_id, error_type, row, topic_id):
    project_id = "elated-scope-437703-h9"
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

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
    print(f"Sent {topic_id} message to job orchestrator.")