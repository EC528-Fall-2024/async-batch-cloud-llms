# Requires pandas and pyarrow to be installed
import sys
from google.cloud import bigquery
import pandas as pd


# Initialize a BigQuery client
client = bigquery.Client()

# Example DataFrame
data = {
    #TODO: Change dataframe based on what the client wants
    "name": ["Alice", "Bob", "Charlie"],
    "age": [25, 30, 37],
}
df = pd.DataFrame(data)

# BigQuery table information
project_id = "elated-scope-437703-h9"
dataset_id = "test_dataset"
table_id = "test_2"

# Define the full table reference
table_ref = f"{project_id}.{dataset_id}.{table_id}"

# Define the table schema
schema = [
    bigquery.SchemaField("name", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("age", "INTEGER", mode="REQUIRED"),
]

# Create the table if it doesn't exist
try:
    table = bigquery.Table(table_ref, schema=schema)
    table = client.create_table(table)  # API request
    print(f"Table {table_ref} created successfully.")
except Exception as e:
    if "Already Exists" in str(e):
        print(f"Table {table_ref} already exists.")
        sys.exit()
    else:
        print(f"\nThe error message is {str(e)}")

# Upload DataFrame to the new table
job = client.load_table_from_dataframe(df, table_ref)
job.result()  # Waits for the job to complete

print(f"Data uploaded to {table_ref} successfully.")
