from google.cloud import bigquery
from ErrorLogger import error_message
import time
import random

def write_response(response, row=1, job_id=1, client_id=1, project_id="elated-scope-437703-h9", dataset_id="test_dataset", table_id="test_table", delay = 0):
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
        print(f"Response for row {row} updated successfully.")
    
    # Error-handling
    except Exception as e:
        # Retry if concurrency writing issue
        if "concurrent update" in str(e):
            wait = random.randint(1,3) # delay before trying to write again
            print(f"Concurrency error updating BigQuery for row {row}: {e}. Trying again after {wait} seconds.")
            write_response(response, row, job_id, client_id ,delay=wait)

        # Drop the current row if unexpected error present
        else:
            message = f"Unexpected error updating BigQuery for row {row}: {e}"
            print(message)
            
            # send message to job orchestrator that this row was dropped
            error_message(message, job_id, client_id, "RowDropped", row, "ErrorLogs") 