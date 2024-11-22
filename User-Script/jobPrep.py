import requests
import logging

# Setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
API_BASE_URL = "https://flask-api-1069651367433.us-central1.run.app"

# Retrive API Key
def retrieve_api_key(user_data):
    auth_data = {"username": user_data["username"], "password": user_data["password"]}
    try:
        headers = { "Content-Type": "application/json" }
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

# Get job data
def get_job_data(user_data):
    return {
        "Client_ID": user_data["Client_ID"],
        "User_Project_ID": user_data["User_Project_ID"],
        "User_Dataset_ID": user_data["User_Dataset_ID"],
        "Input_Table_ID": user_data["Input_Table_ID"],
        "Output_Table_ID": user_data["Output_Table_ID"],
        "Model": user_data["Model"],
        "API_key": user_data["API_key"]
    }

# Submit job
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