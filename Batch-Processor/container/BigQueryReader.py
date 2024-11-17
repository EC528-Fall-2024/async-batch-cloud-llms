from google.cloud import bigquery


# This function will query the Big Query Table given a row. It will return the value of "prompt_and_text"
# Inputs: 
# Passed Parameter row

# Testing
# In Project Contents:
# project_id = "elated-scope-437703-h9"
# dataset_id = "test_dataset"
# table_id = "test_table"

# Andrew's Out Of Project Contents:
# project_id = "sampleproject-440900"
# dataset_id = "11_05_dataset"
# table_id = "testing-purposes"

# Noah's Other out of project contents: sailing-map-411015.user_dataset.input_table
# project_id = "sailing-map-411015"
# dataset_id = "user_dataset"
# table_id = "input_table"


# Outputs: prompt_and_text
# def read_from_database(row, project_id = "elated-scope-437703-h9", dataset_id = "test_dataset", table_id = "test_table"):
def read_from_database(row, project_id = "sampleproject-440900", dataset_id = "user_dataset", table_id = "input_table"):
#def read_from_database(row, project_id = "elated-scope-437703-h9", dataset_id = "test_dataset", table_id = "test_table"):


    # Initialize BigQuery client
    client = bigquery.Client(project=project_id)

    # Construct the fully qualified table ID
    full_table_id = f"{project_id}.{dataset_id}.{table_id}"

    # SQL query to select only plain_text column for the specified row
    query = f"""
        SELECT prompt_and_text
        FROM `{full_table_id}`
        WHERE row = {row}
        LIMIT 1
    """
    print(f"Value of query is {query}")

    # Set up query parameters
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("row", "STRING", row)
        ]
    )

    # Run the query and fetch results
    try:
        query_job = client.query(query, job_config=job_config)
        results = query_job.result()  # Wait for the job to complete

        # Get the single row result
        for row in results:
            return row.prompt_and_text
        
        return None  # Return None if no row is found

    except Exception as e:
        print(f"Error querying BigQuery: {e}")
        return None
    
if __name__ == "__main__":
    read_from_database(row=1)