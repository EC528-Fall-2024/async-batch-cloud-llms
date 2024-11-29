from google.cloud import bigquery
from Logger import log

# Get database length
def get_database_length(project_id, dataset_id, table_id):
    try:
        client = bigquery.Client(project=project_id)
        query = f"SELECT COUNT(*) as total FROM `{project_id}.{dataset_id}.{table_id}`"
        query_job = client.query(query)
        results = query_job.result()
        for row in results:
            return row.total
        
    except Exception as e:
        print(f"Error getting database length: {e}")

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
            return row.prompt_and_text
        
        return None  # Return None if no row is found

    # Drop the current row if unexpected error present
    except Exception as e:
        message = f"Unexpected error querying BigQuery for row {row}: {e}"
        print(message)

        # send message to job orchestrator that this row was dropped
        log(message, Job_ID, Client_ID, "RowDropped", row)
        return None