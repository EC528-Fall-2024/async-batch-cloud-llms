import requests
import time
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def retrieve_api_key():
    username = user_data["username"]
    password = user_data["password"]

    auth_data = {"username": username, "password": password}
    try:
        response = requests.post(f"{API_BASE_URL}/get_api_key", json=auth_data, headers=headers, timeout=10)
        if response.status_code == 200:
            api_key = response.json().get("api_key")
            logging.info(f"API key retrieved successfully: {api_key}")
            headers["x-api-key"] = api_key
            return api_key
        else:
            logging.error(f"Error retrieving API key: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Network error while retrieving API key: {e}")
        return None

def get_job_data():
    return {
        "Client_ID": user_data["Client_ID"],
        "User_Project_ID": user_data["User_Project_ID"],
        "User_Dataset_ID": user_data["User_Dataset_ID"],
        "Input_Table_ID": user_data["Input_Table_ID"],
        "Output_Table_ID": user_data["Output_Table_ID"],
        "Model": user_data["Model"],
        "API_key": user_data["API_key"]
    }

def submit_job(api_key, job_data):
    headers = {
        "x-api-key": api_key
    }
    response = requests.post(f"{API_BASE_URL}/submit_job", headers=headers, json=job_data)
    if response.status_code == 200:
        logging.info("Job submitted successfully.")
        # Correct the key name here to match the response from /submit_job endpoint
        return response.json().get('Job_ID')
    else:
        logging.error(f"Error submitting job: {response.status_code} - {response.text}")
        return None
    
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
