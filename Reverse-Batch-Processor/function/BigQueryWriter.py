from google.cloud import bigquery
from Logger import log
import time
import random

def insert_rows(response, row, job_id, client_id, project_id="your-project-id", dataset_id="your-dataset", table_id="your-table", delay=0):
    time.sleep(delay)
    client = bigquery.Client(project=project_id)
    table_ref = client.dataset(dataset_id).table(table_id)

    rows_to_insert = [
        {
            "response": response,
            "row": row
        }
    ]

    # Try to insert rows directly into the table
    try:
        errors = client.insert_rows_json(table_ref, rows_to_insert)  # API request
        # Check if row-level writing error occurred
        if errors:
            message = f"Encountered errors for updating row {row}:\n {errors}"
            print(message)
            log(message, job_id, client_id, "RowDropped", row, "ErrorLogs") # send message to job orchestrator

        # Successfully updated rows
        else:
            print(f"Response for row {row} updated successfully")
    
    except Exception as e:
        # Retry if concurrency writing issue
        if "concurrent update" in str(e):
            wait = random.randint(1,3) # delay before trying to write again
            print(f"Concurrency error updating BigQuery for row {row}: {e}. Trying again after {wait} seconds.")
            insert_rows(response, row, job_id, client_id, project_id, dataset_id, table_id, delay=wait)

        # Drop the current row if unexpected error present
        else:
            message = f"Unexpected error updating BigQuery for row {row}: {e}"
            print(message)
            log(message, job_id, client_id, "RowDropped", row) # send message to job orchestrator