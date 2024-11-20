import requests
import json

url = "https://us-central1-elated-scope-437703-h9.cloudfunctions.net/batch-processor-http"

def call_batch_processor(job_id, client_id, project, dataset, input_table, output_table, model, api_key):
    try:
        payload = json.dumps({
            "Job_ID": f"{job_id}",
            "Client_ID": f"{client_id}",
            "User_Project_ID": f"{project}",
            "User_Dataset_ID": f"{dataset}",
            "Input_Table_ID": f"{input_table}",
            "Output_Table_ID": f"{output_table}",
            "Model": f"{model}",
            "API_key": f"{api_key}"
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(f"Received response from batch processor: {response.text}")
    except Exception as e:
        print(f"Unexpected error invoking batch processor: {e}")
