import logging
import json
from .jobPrep import retrieve_api_key, get_job_data, submit_job
from .jobStatus import wait_for_completion

def submitjob(username, password, Client_ID, User_Project_ID, User_Dataset_ID, Input_Table_ID, Output_Table_ID, Model, API_key):
    # turn inputs into dict
    user_data = {
        "username": username,
        "password": password,
        "Client_ID": Client_ID,
        "User_Project_ID": User_Project_ID,
        "User_Dataset_ID": User_Dataset_ID,
        "Input_Table_ID": Input_Table_ID,
        "Output_Table_ID": Output_Table_ID,
        "Model": Model,
        "API_key": API_key
    }

    # Step 1: Retrieve API Key
    logging.info("🔑 Retrieving API key...")
    api_key = retrieve_api_key(user_data)

    # Step 2: Prepare and Submit Job
    if api_key:
        logging.info("📋 Preparing job data...")
        job_data = get_job_data(user_data)
        logging.info("📤 Submitting job...")
        job_id = submit_job(api_key, job_data)

        # # The code below would enable a continuous status pull until job completion
        # # Step 3: Monitor Job Status
        # if job_id:
        #     logging.info("⏳ Monitoring job status...")
        #     final_status = wait_for_completion(
        #         job_id, user_data["Client_ID"], api_key, 3)
        #     if final_status:
        #         logging.info("📊 Final Job Status Retrieved:")
        #         logging.info(json.dumps(final_status, indent=4))
    
    return job_id, api_key
