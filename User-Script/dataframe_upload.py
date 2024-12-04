import sys
import google
from google.cloud import bigquery
import pandas as pd

def CSV_to_BigQuery(CSV_path, project_id, dataset_id, table_id, output_table_id):

    # Connect to BigQuery client in project
    client = bigquery.Client(project=project_id)

    # CSV to DF
    df = pd.read_csv(CSV_path)

    # Define table parameters
    input_table_ref = f"{project_id}.{dataset_id}.{table_id}"
    input_schema = [
        bigquery.SchemaField("row", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("prompt_and_text", "STRING", mode="REQUIRED"),
    ]

    output_table_ref = f"{project_id}.{dataset_id}.{output_table_id}"
    output_schema = [
        bigquery.SchemaField("row", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("response", "STRING", mode="REQUIRED"),
    ]

    # Create the dataset if it doesn't exist
    dataset_ref = client.dataset(dataset_id) 
    dataset = bigquery.Dataset(dataset_ref) 
    dataset.location = "US" # Set location as needed
    try: 
        client.get_dataset(dataset_ref) 
        print(f"Dataset {dataset_id} already exists.") 

    except google.api_core.exceptions.NotFound: 
        dataset = client.create_dataset(dataset) 
        print(f"Dataset {dataset_id} created successfully.")

    # Create new output datatable
    try:
        table = bigquery.Table(output_table_ref, schema=output_schema)
        table = client.create_table(table)
        print(f"Table {output_table_ref} created successfully.")
    except Exception as e:
        if "Already Exists" in str(e):
            print(f"Table {output_table_ref} already exists.")
        else:
            print(f"\nThe error message is {str(e)}")

    # Creates new input datatable
    try:
        table = bigquery.Table(input_table_ref, schema=input_schema)
        table = client.create_table(table)
        print(f"Table {input_table_ref} created successfully.")
    except Exception as e:
        if "Already Exists" in str(e):
            print(f"Table {input_table_ref} already exists.")
            sys.exit()
        else:
            print(f"\nThe error message is {str(e)}")

    job = client.load_table_from_dataframe(df, input_table_ref)
    job.result()

    print(f"Data uploaded to {input_table_ref} successfully.")
