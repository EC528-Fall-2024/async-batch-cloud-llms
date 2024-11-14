from google.cloud import bigquery
from google.cloud import pubsub_v1
import time
import random

microservice = "ReverseBatchProcessor"

# send log messages to job orchestrator
def log_message(message, job_id, client_id, row, topic_id):
    project_id = "elated-scope-437703-h9"
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    message = f"{message}".encode("utf-8")
    
    # Define attributes as a dictionary
    attributes = {
        "Job_ID": f"{job_id}",
        "Client_ID": f"{client_id}",
        "Microservice:": f"{microservice}",
        "Row_Number": f"{row}"
    }

    publisher.publish(topic_path, message, **attributes)
    print(f"Sent {topic_id} message to job orchestrator.")

def write_response(response: str, row: int, job_id, client_id, project_id="elated-scope-437703-h9", dataset_id="test_dataset", table_id="test_table", delay = 0):
    time.sleep(delay)
    # Initialize BigQuery client
    client = bigquery.Client(project=project_id)

    # Construct the fully qualified table ID
    full_table_id = f"{project_id}.{dataset_id}.{table_id}"

    # SQL query to update the response column for the specified row
    query = f"""
        UPDATE `{full_table_id}`
        SET response = @response
        WHERE row = @row
    """

    # Set up query parameters
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("response", "STRING", response),
            bigquery.ScalarQueryParameter("row", "INT64", row)  # Assuming row is of INT64 type
        ]
    )

    # Run the update query
    try:
        query_job = client.query(query, job_config=job_config)
        query_job.result()  # Wait for the job to complete
        message=f"Response for row {row} updated successfully."
        print(message)
        log_message(message, job_id, client_id, row, "ProgressLogs") # send message to job orchestrator
    except Exception as e:
        wait = random.randint(1,10)
        message = f"Error updating BigQuery for row {row}: {e}. Trying again after {wait} seconds."
        print(message)
        log_message(message, job_id, client_id, row, "ErrorLogs") # send message to job orchestrator
        write_response(response, row, job_id, client_id ,delay=wait)

# Testing locally
# sampleproject-440900.user_dataset.output_response
if __name__ == "__main__":
    write_response("This is a dummy response!","1",1,"client_1",project_id="sampleproject-440900", dataset_id="user_dataset", table_id="output_response")