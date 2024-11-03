from google.cloud import bigquery
from testSinglePubSubSender import pubSubSender

def query_bigquery(row_id, project_id = "elated-scope-437703-h9", dataset_id = "test_dataset", table_id = "test_table_with_rows"):
    """
    Queries a BigQuery table and returns the plain_text column for a specific row.
    """
    
    # Initialize BigQuery client
    client = bigquery.Client(project=project_id)

    # Construct the fully qualified table ID
    full_table_id = f"{project_id}.{dataset_id}.{table_id}"

    # SQL query to select only plain_text column for the specified row
    query = f"""
        SELECT plain_text
        FROM `{full_table_id}`
        WHERE row_number = {row_id}
        LIMIT 1
    """

    # Set up query parameters
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("row_number", "STRING", row_id)
        ]
    )

    # Run the query and fetch results
    try:
        query_job = client.query(query, job_config=job_config)
        results = query_job.result()  # Wait for the job to complete

        # Get the single row result
        for row in results:
            return row.plain_text
        
        return None  # Return None if no row is found

    except Exception as e:
        print(f"Error querying BigQuery: {e}")
        return None
    
def remove_plain_text_prefix(text):
    prefix = "Plain text: "
    if text.startswith(prefix):
        return text[len(prefix):]
    return text

# Example usage
if __name__ == "__main__":
    project_id = "elated-scope-437703-h9"
    dataset_id = "test_dataset"
    table_id = "test_table_with_rows"
    row_id = 2  # Replace with the actual row ID you want to query
    
    result = query_bigquery(row_id)
    if result:
        pubSubSender(result)
        print(f"Plain text: {(result)}")
    else:
        print("No result found or an error occurred")