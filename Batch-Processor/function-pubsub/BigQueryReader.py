from google.cloud import bigquery

# Steps
# 1. Move the handle go to this file
# Add Logging function

#GeneralLogs
#ProgressLogs
#ErrorLogs

## Progress Format
# Topic: ProgressLogs
# message=f"Prompt and Text for row {row} read successfully."


## Error Logs Format
# Topic: ErrorLogs
##message = f"Error Reading BigQuery for row {row}: {e}."



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



# Outputs: prompt_and_text
def read_from_database(row, project_id = "elated-scope-437703-h9", dataset_id = "test_dataset", table_id = "test_table"):
# def read_from_database(row, project_id = "sampleproject-440900", dataset_id = "user_dataset", table_id = "input_table"):
#def read_from_database(row, project_id = "elated-scope-437703-h9", dataset_id = "test_dataset", table_id = "test_table"):

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
        
        message=f"Prompt and Text for row {row} read successfully."
        log_message(message, job_id, client_id, row, topic_id)
        
        return None  # Return None if no row is found

    except Exception as e:
        (f"Error querying BigQuery: {e}")
        return None

# sampleproject-440900.user_dataset.input_table
# if __name__ == "__main__":
#     read_from_database(row=1, project_id="sampleproject-440900",dataset_id='user_dataset',table_id='input_table')


# Testing for out of Project Tables

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