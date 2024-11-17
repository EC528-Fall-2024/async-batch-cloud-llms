import requests
import time

API_BASE_URL = "https://flask-api-1069651367433.us-east4.run.app"
API_KEY = "secret-api-key"

headers = {
    "Content-Type": "application/json",
}

def submit_job():
    job_data = {
        "client_id":  "example_client",
        "project_id": "example_project_id",
        "dataset_id": "example_dataset_id",
        "table_id": "example_table_id",
        "table_key": {},
        "row_count": 13,
        "request_column": 0,
        "response_column": 1,
        "llm_model": "gpt-3.5",
        "prompt_prefix": "example_prefix",
        "prompt_postfix": "example_postfix"
    }
    
    response = requests.post(f"{API_BASE_URL}/submit_job", json=job_data, headers=headers)
    
    if response.status_code == 200:
        return response.json()['job_id']
    else:
        print(f"Error submitting job: {response.text}")
        return None


def main():
    # Submit a job
    job_id = submit_job()
 
    if job_id:
        print(f"Job submitted successfully. Job ID: {job_id}")
      
        # Poll for job status
        #while True:
        #    status = check_job_status(job_id)
        #   if status:
        #        print(f"Job status: {status['status']}")
        #       if status['status'] == "completed":
        #            print("Job completed successfully!")
        #            break
        #    time.sleep(5)  # Wait for 5 seconds before checking again


if __name__ == "__main__":
    main()