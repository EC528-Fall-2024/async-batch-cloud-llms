import requests
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def retrieve_api_key(API_BASE_URL, username, password):
    """
    Retrieve an API key using the provided username and password.

    Parameters:
    - API_BASE_URL: The base URL of the API.
    - username: The user's username.
    - password: The user's password.

    Returns:
    - The API key as a string, or None if authentication fails.
    """
    auth_data = {"username": username, "password": password}
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(f"{API_BASE_URL}/get_api_key", json=auth_data, headers=headers, timeout=10)
        if response.status_code == 200:
            api_key = response.json().get("api_key")
            logging.info(f"API key retrieved successfully: {api_key}")
            return api_key
        else:
            logging.error(f"Error retrieving API key: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Network error while retrieving API key: {e}")
        return None


def get_job_data(user_data, api_key):
    """
    Prepare job data for submission.

    Parameters:
    - user_data: A dictionary containing user-specific data.
    - api_key: The API key to include in the job data.

    Returns:
    - A dictionary representing the job data.
    """
    return {
        "Client_ID": user_data["Client_ID"],
        "User_Project_ID": user_data["User_Project_ID"],
        "User_Dataset_ID": user_data["User_Dataset_ID"],
        "Input_Table_ID": user_data["Input_Table_ID"],
        "Output_Table_ID": user_data["Output_Table_ID"],
        "Model": user_data["Model"],
        "API_key": api_key
    }


def submit_job(API_BASE_URL, api_key, job_data):
    """
    Submit a job to the API.

    Parameters:
    - API_BASE_URL: The base URL of the API.
    - api_key: The API key for authentication.
    - job_data: The job data to submit.

    Returns:
    - The Job ID if successful, None otherwise.
    """
    headers = {
        "x-api-key": api_key
    }
    response = requests.post(f"{API_BASE_URL}/submit_job", headers=headers, json=job_data)
    if response.status_code == 200:
        logging.info("Job submitted successfully.")
        return response.json().get('Job_ID')
    else:
        logging.error(f"Error submitting job: {response.status_code} - {response.text}")
        return None
    
def check_job_status(API_BASE_URL, job_id, client_id, api_key):
    headers = {"x-api-key": api_key}
    params = {"Client_ID": client_id}
    
    response = requests.get(f"{API_BASE_URL}/job_status/{job_id}", headers=headers, params=params)

    if response.status_code == 200:
        job_data = response.json()
        logging.info(f"Raw Response: {job_data}")
        current_row = job_data.get('current_row', 0)
        total_rows = job_data.get('total_rows', 0)

        if current_row >= total_rows:
            logging.info(f"Job {job_id} is complete. Processed {current_row} rows.")
            return {"status": "complete", "details": job_data}
        else:
            logging.info(f"Job {job_id} in progress: {current_row} / {total_rows}")
            return {"status": "in_progress", "details": job_data}
    else:
        logging.error(f"Failed to retrieve job status: {response.status_code}, {response.text}")
        return None



def wait_for_completion(API_BASE_URL, job_id, client_id, api_key, interval=10):
    """
    Check the job status repeatedly until it is complete.

    Parameters:
    - API_BASE_URL: The base URL of the API.
    - job_id: The ID of the job to check.
    - client_id: The ID of the client who submitted the job.
    - api_key: The API key for authentication.
    - interval: Time (in seconds) to wait between status checks.

    Returns:
    - The final job status details.
    """
    while True:
        job_status = check_job_status(API_BASE_URL, job_id, client_id, api_key)

        if job_status:
            if job_status["status"] == "complete":
                logging.info("✅ Job processing is complete.")
                return job_status["details"]
            elif job_status["status"] == "in_progress":
                logging.info("⏳ Job is still in progress. Retrying in a few seconds...")
        else:
            logging.error("❌ Could not retrieve job status. Retrying...")

        time.sleep(interval)