from google.cloud import pubsub_v1

project_id = "elated-scope-437703-h9"
microservice = "ReverseBatchProcessor"

# send log messages to job orchestrator
def log(message, job_id, client_id, error_type, row):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, "Status")

    message = f"{message}".encode("utf-8")

    # Define attributes as a dictionary
    attributes = {
        "Log_Type": "Error",
        "Microservice": f"{microservice}",
        "Job_ID": f"{job_id}",
        "Client_ID" : f"{client_id}",
        "Row_Number": f"{row}",
        "Num_Rows" : "", # empty since error log
        "Error_Type": f"{error_type}",
    }

    publisher.publish(topic_path, message, **attributes)
    print(f"Sent error log message to job orchestrator.")

# send time metrics to status collector
def send_metrics(client_id, job_id, row, end, final_row):
    publisher = pubsub_v1.PublisherClient()
    publisher_path = publisher.topic_path(project_id, "Stats")

    # Prepare message to publish
    service = "ReverseBatchProcessor"
    message = service.encode("utf-8")
    attributes = {
        "Job_ID": f"{job_id}",
        "Client_ID": f"{client_id}",
        "Row": f"{row}",
        "Start": "",
        "In_LLM": "",
        "Out_LLM": "",
        "End": str(end),
        "Final_Row_Flag": str(final_row)
    }

    # Send out response via pub/sub
    publisher.publish(publisher_path, message, **attributes)
    print("Sent time metrics to stats collector") 