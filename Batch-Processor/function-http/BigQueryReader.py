from google.cloud import bigquery
from Logger import log

# Outputs: prompt_and_text
def read_from_database(row, Job_ID, Client_ID, project_id, dataset_id, table_id):
    
    # Initialize BigQuery client
    client = bigquery.Client(project=project_id)
    full_table_id = f"{project_id}.{dataset_id}.{table_id}"

    # SQL query to select only plain_text column for the specified row
    query = f"""
        SELECT prompt_and_text
        FROM `{full_table_id}`
        WHERE row = {row}
        LIMIT 1
    """

    # Set up query parameters
    job_config = bigquery.QueryJobConfig(query_parameters=[bigquery.ScalarQueryParameter("row", "STRING", row)])

    # Run the query and fetch results
    try:
        query_job = client.query(query, job_config=job_config)
        results = query_job.result()  # Wait for the job to complete

        # Get the single row result
        for row in results:
            print("///////")
            print(f"{row}")
            print("///////")
            # print(f"Prompt and Text for row {row} read successfully.")
            return row.prompt_and_text
        
        return None  # Return None if no row is found

    # Drop the current row if unexpected error present
    except Exception as e:
        message = f"Unexpected error querying BigQuery for row {row}: {e}"
        print(message)

        # send message to job orchestrator that this row was dropped
        log(message, Job_ID, Client_ID, "RowDropped", row)
        return None

# # Need to update permissions to BQ Data View and BQ Job User
# if __name__ == "__main__":
#     read_from_database(row=1, Job_ID=1, Client_ID=1,project_id="sampleproject-440900",dataset_id='user_dataset',table_id='input_table')