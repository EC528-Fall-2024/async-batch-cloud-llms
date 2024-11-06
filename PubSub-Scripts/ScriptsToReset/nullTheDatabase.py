from google.cloud import bigquery

def write_response(row, response, project_id="elated-scope-437703-h9", dataset_id="test_dataset", table_id="test_table"):
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
        print("Response updated successfully.")
    except Exception as e:
        print(f"Error updating BigQuery: {e}")

# Example usage:
for i in range(1 , 14): # change 14 if the size is diferent
    write_response(i, "null")

