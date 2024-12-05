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
    Check the status of a job using its Job ID and Client ID.

    Parameters:
    - job_id: The Job ID returned from the `/submit_job` endpoint.
    - client_id: The Client ID associated with the job.
    - api_key: The API key retrieved earlier in the script.

    Returns:
    - A dictionary with job status or a completion message.
    """

    logging.info("🔎 Checking for Job Status...")

    headers = {
        "x-api-key": api_key  # Use the already retrieved API key
    }
    params = {
        "Client_ID": client_id  # Ensure the `Client_ID` is passed as required
    }

    response = requests.get(f"{API_BASE_URL}/job_status/{job_id}", headers=headers, params=params)

    if response.status_code == 200:
        job_data = response.json()
        current_row = job_data.get('current_row', 0)
        total_rows = job_data.get('total_rows', 0)

        # Check if the job is complete
        if current_row >= total_rows:
            logging.info(f"Job {job_id} is complete. Processed {current_row} rows.")
            return {
                "status": "complete",
                "details": job_data
            }
        else:
            logging.info(f"Job {job_id} in progress: {current_row} / {total_rows}")
            return {
                "status": "in_progress",
                "details": job_data
            }
    else:
        logging.error(f"Failed to retrieve job status: {response.status_code}, {response.text}")
        return None