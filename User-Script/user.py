import requests
import time
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


API_BASE_URL = "https://flask-api-1069651367433.us-east4.run.app"
headers = {
    "Content-Type": "application/json",
}

def retrieve_api_key():
    """
    Retrieve API key from the Flask API using username and password.
    """
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    auth_data = {"username": username, "password": password}
    try:
        response = requests.post(f"{API_BASE_URL}/get_api_key", json=auth_data, headers=headers, timeout=10)
        if response.status_code == 200:
            api_key = response.json().get("api_key")
            logging.info(f"API key retrieved successfully: {api_key}")
            # Update headers to include the API key for future requests
            headers["x-api-key"] = api_key
            return api_key
        else:
            logging.error(f"Error retrieving API key: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Network error while retrieving API key: {e}")
        return None

def get_job_data_from_user():
    # Collect job information from the user
    client_id = input("Enter client ID: ")
    project_id = input("Enter project ID: ")
    dataset_id = input("Enter dataset ID: ")
    table_id = input("Enter table ID: ")
    table_key = input("Enter table key (as JSON object): ") or "{}"
    row_count = int(input("Enter row count: "))
    request_column = int(input("Enter request column index: "))
    response_column = int(input("Enter response column index: "))
    llm_model = input("Enter LLM model (e.g., gpt-3.5): ")
    prompt_prefix = input("Enter prompt prefix: ")
    prompt_postfix = input("Enter prompt postfix: ")

    # Prepare job data
    return {
        "client_id": client_id,
        "project_id": project_id,
        "dataset_id": dataset_id,
        "table_id": table_id,
        "table_key": table_key,
        "row_count": row_count,
        "request_column": request_column,
        "response_column": response_column,
        "llm_model": llm_model,
        "prompt_prefix": prompt_prefix,
        "prompt_postfix": prompt_postfix,
    }

def submit_job():
    job_data = get_job_data_from_user()

    try:
        response = requests.post(f"{API_BASE_URL}/submit_job", json=job_data, headers=headers, timeout=10)
        if response.status_code == 200:
            logging.info("Job submitted successfully.")
            return response.json()['job_id']
        else:
            logging.error(f"Error submitting job: {response.status_code} - {response.text}")
            return None

    except requests.exceptions.RequestException as e:
        logging.error(f"Network error occurred: {e}")
        return None

def check_job_status(job_id):
    try:
        response = requests.get(f"{API_BASE_URL}/job_status/{job_id}", headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            logging.warning(f"Job with ID {job_id} not found.")
        else:
            logging.error(f"Failed to retrieve job status: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Network error while checking job status: {e}")
    return None

def main():
    api_key = retrieve_api_key()

    if not api_key:
        logging.error("Failed to retrieve API key. Exiting...")
        return
    
    job_id = submit_job()
 
    if job_id:
        logging.info(f"Job ID: {job_id}")

        # Poll for job status with an exponential backoff strategy
        backoff_time = 30 # Initial backoff time in seconds
        max_backoff_time = 3600  # Maximum backoff time in seconds (60 minutes)
        max_attempts = 10  # Maximum number of attempts to poll job status

        attempts = 0
        while attempts < max_attempts:
            status = check_job_status(job_id)
            if status:
                logging.info(f"Job status: {status['status']}")
                if status['status'] == "completed":
                    logging.info("Job completed successfully!")
                    break
                elif status['status'] == "processing":
                    logging.info("Job is still processing. Checking again in a few seconds...")
            else:
                logging.warning("Failed to retrieve job status. Retrying...")

            # Wait before the next attempt with an exponential backoff
            time.sleep(backoff_time)
            backoff_time = min(backoff_time * 2, max_backoff_time)
            attempts += 1

        if attempts == max_attempts:
            logging.error("Maximum number of attempts reached. Job status check terminated.")

if __name__ == "__main__":
    main()
