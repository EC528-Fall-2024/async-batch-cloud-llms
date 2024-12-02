# Requires pandas and pyarrow to be installed
import sys
from google.cloud import bigquery
import pandas as pd


client = bigquery.Client()

############################################################################################################
#TODO: Change dataframe based on what the client wants
data = {
    "name": ["Alice", "Bob", "Charlie"],
    "age": [25, 30, 37],
}
############################################################################################################

df = pd.DataFrame(data)

############################################################################################################
#TODO: Change BQT location
project_id = "elated-scope-437703-h9"
dataset_id = "test_dataset"
table_id = "test_2"
############################################################################################################

# Define the full table reference
table_ref = f"{project_id}.{dataset_id}.{table_id}"

############################################################################################################
#TODO: Change the schema for what the information should be for LLM
schema = [
    bigquery.SchemaField("name", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("age", "INTEGER", mode="REQUIRED"),
]
############################################################################################################


# Creates a new datatable if it doesn't exist, otherwise just quits
try:
    table = bigquery.Table(table_ref, schema=schema)
    table = client.create_table(table)
    print(f"Table {table_ref} created successfully.")
except Exception as e:
    if "Already Exists" in str(e):
        print(f"Table {table_ref} already exists.")
        sys.exit()
    else:
        print(f"\nThe error message is {str(e)}")

job = client.load_table_from_dataframe(df, table_ref)
job.result()

print(f"Data uploaded to {table_ref} successfully.")
