import logging
import requests
import time

# Setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
API_BASE_URL = "https://flask-api-1069651367433.us-central1.run.app"

# Check status until job completed
def wait_for_completion(job_id, client_id, api_key, interval=10):
    """
    Check the job status repeatedly until it is complete.

    Parameters:
    - job_id: The ID of the job to check.
    - client_id: The ID of the client who submitted the job.
    - api_key: The API key retrieved earlier.
    - interval: Time (in seconds) to wait between status checks.

    Returns:
    - The final job status details.
    """
    while True:
        # Use the updated `check_job_status` function
        job_status = check_job_status(job_id, client_id, api_key)

        if job_status:
            if job_status["status"] == "complete":
                logging.info("✅ Job processing is complete.")
                return job_status["details"]  # Return the final status
            elif job_status["status"] == "in_progress":
                logging.info("⏳ Job is still in progress. Retrying in a few seconds...")
        else:
            logging.error("❌ Could not retrieve job status. Retrying...")

        # Wait for the specified interval before checking again
        time.sleep(interval)

# Check status manually   
def check_job_status(job_id, client_id, api_key):
    """
    Check the status of a job, including error details, using its Job ID and Client ID.

    Parameters:
    - job_id: The Job ID returned from the `/submit_job` endpoint.
    - client_id: The Client ID associated with the job.
    - api_key: The API key retrieved earlier in the script.

    Returns:
    - A dictionary with job status, progress, and error details.
    """
    logging.info(f"🔎 Fetching status for job {job_id}...")

    headers = {
        "x-api-key": api_key
    }
    params = {
        "Client_ID": client_id
    }

    response = requests.get(f"{API_BASE_URL}/job_status/{job_id}", headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        logging.info("✅ Job status retrieved successfully.")

        # Display the job status
        print("Job Status:")
        print(f"Job ID: {data['Job_ID']}")
        print(f"Progress: {data['current_row']} / {data['total_rows']}")
        if data["errors_present"]:
            print("Errors Found:")
            for row in data["error_rows"]:
                print(f" - Error at row: {row}")
        else:
            print("No errors detected.")

        # Return detailed status
        return data
    else:
        logging.error(f"Failed to fetch job status: {response.status_code}, {response.text}")
        return None