import requests
import time

API_BASE_URL = "http://localhost:5000"
API_KEY = "your-secret-api-key"

headers = {
    "Content-Type": "application/json",
    "X-API-Key": API_KEY
}

def submit_job(input_bucket_url, output_bucket_url, input_format, input_file_name, output_format, llm_model):
    job_data = {
        "input_bucket_url": input_bucket_url,
        "output_bucket_url": output_bucket_url,
        "input_format": input_format,
        "input_file_name": input_file_name,
        "output_format": output_format,
        "llm_model": llm_model
    }
    
    response = requests.post(f"{API_BASE_URL}/submit_job", json=job_data, headers=headers)
    
    if response.status_code == 200:
        return response.json()['job_id']
    else:
        print(f"Error submitting job: {response.text}")
        return None

def check_job_status(job_id):
    response = requests.get(f"{API_BASE_URL}/job_status/{job_id}", headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error checking job status: {response.text}")
        return None

def main():
    # Submit a job
    job_id = submit_job(
        input_bucket_url="https://storage.googleapis.com/input-bucket",
        output_bucket_url="https://storage.googleapis.com/output-bucket",
        input_format="csv",
        input_file_name="data.csv",
        output_format="json",
        llm_model="gpt-3.5-turbo"
    )
 
    if job_id:
        print(f"Job submitted successfully. Job ID: {job_id}")
      
        # Poll for job status
        while True:
            status = check_job_status(job_id)
            if status:
                print(f"Job status: {status['status']}")
                if status['status'] == "completed":
                    print("Job completed successfully!")
                    break
            time.sleep(5)  # Wait for 5 seconds before checking again


if __name__ == "__main__":
    main()