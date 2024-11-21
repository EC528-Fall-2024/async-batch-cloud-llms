from flask import Flask, request, jsonify
import uuid
import time
import json
import os
import requests
from google.cloud import pubsub_v1
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['DEBUG'] = os.environ.get('FLASK_DEBUG')

# Example user database
USERS = {"test_user": "test_password"}
API_KEYS = {}  # Store API keys for simplicity; consider using a database in production


# Set up pub/sub publisher for IncomingJob topic
project_id = "elated-scope-437703-h9"
topic_id = "IncomingJob"

publisher = pubsub_v1.PublisherClient()
# The `topic_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/topics/{topic_id}`
topic_path = publisher.topic_path(project_id, topic_id)

# Helper function for API key validation
def require_api_key(func):
    def wrapper(*args, **kwargs):
        api_key = request.headers.get("x-api-key")
        if api_key not in API_KEYS.values():
            return jsonify({"error": "Unauthorized. Invalid API key."}), 401
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__  # Ensure Flask can identify the route's name
    return wrapper

@app.route('/get_api_key', methods=['POST'])
def get_api_key():
    auth_data = request.json
    username = auth_data.get("username")
    password = auth_data.get("password")

    # Authenticate user
    if USERS.get(username) == password:
        # Generate and store an API key
        api_key = str(uuid.uuid4())
        API_KEYS[username] = api_key
        return jsonify({"api_key": api_key}), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401

# Function for submitting job
def publish_job(job_data, job_id): 
    # Hardcoded message
    message = "IncomingJob".encode("utf-8")
    
    # Define attributes to pass to Pub/Sub
    attributes = {
        "Job_ID": job_id,
        "Client_ID": job_data["Client_ID"],
        "User_Project_ID": job_data["User_Project_ID"],
        "User_Dataset_ID": job_data["User_Dataset_ID"],
        "Input_Table_ID": job_data["Input_Table_ID"],
        "Output_Table_ID": job_data["Output_Table_ID"],
        "Model": job_data["Model"],
        "API_key": job_data["API_key"]
    }

    # Publish the message
    future = publisher.publish(topic_path, message, **attributes)
    print(f"Published message with ID: {future.result()}")


# Function for checking if job_data is valid
def check_valid_job(job_data):
    if job_data is not None:
        return True
    else:
        return False


# @app.route('/submit_job', methods=['POST'])
# @require_api_key
# def submit_job():
#     """
#     Updated implementation to call the batch processor directly
#     """
#     job_data = request.json
#     if check_valid_job(job_data):
#         # Generate job ID
#         job_id = str(uuid.uuid4())

#         # Call batch processor
#         payload = {

#             "Job_ID": job_id,
#             "Client_ID": "rick sorkin",
#             "User_Project_ID": "sampleproject-440900",
#             "User_Dataset_ID": "user_dataset",
#             "Input_Table_ID": "input_table",
#             "Output_Table_ID": "output_2",
#             "Model": "gpt-3.5-turbo",
#             "API_key": ""

#             # "Job_ID": job_id,
#             # "Client_ID": job_data.get("client_id", "rick sorkin"),
#             # "User_Project_ID": job_data.get("project_id", "sampleproject-440900"),
#             # "User_Dataset_ID": job_data.get("dataset_id", "user_dataset"),
#             # "Input_Table_ID": job_data.get("table_id", "input_table"),
#             # "Output_Table_ID": job_data.get("output_table_id", "output_2"),
#             # "Model": job_data.get("llm_model", "gpt-3.5-turbo"),
#             # "API_key": job_data.get("api_key", ""),
#         }
#         headers = {'Content-Type': 'application/json'}

#         try:
#             response = requests.request("POST", BATCH_PROCESSOR_URL, headers=headers, data=payload)
#             response_data = response.json()
#         except requests.exceptions.RequestException as e:
#             return jsonify({"error": "Failed to call batch processor", "details": str(e)}), 500

#         # Log response and return job submission status
#         print(response_data)
#         return jsonify({"job_id": job_id, "status": "submitted", "batch_processor_response": response_data}), 200
#     else:
#         return jsonify({"error": "Job not valid"}), 400

# Original implementation (commented out for future use using pub/sub)  
@app.route('/submit_job', methods=['POST'])
@require_api_key
def submit_job():
    """
    Original implementation that uses Pub/Sub and notifies batch processor
    """
    job_data = request.json
    if (check_valid_job(job_data)):
        # If valid, generate job ID, post job, and notify batch processor
        job_id = str(uuid.uuid4())
        publish_job(job_data, job_id)

        # Return job ID to user and indicate that job is submitted
        return jsonify({"job_id": job_id, "status": "submitted"}), 200
    else:
        # Job was not valid
        return jsonify({"error": "Job not valid"}), 400



# Route for checking 
@app.route('/job_status/<job_id>', methods=['GET'])
@require_api_key
def job_status(job_id):
    """
    Get the status of a job, including counts and timing data.
    """
    return 0
    # try:
    #     # Firestore client
    #     db = firestore.Client()
        
    #     # Retrieve counts from Firestore
    #     count_data = getAllFirestore(db, job_id)
        
    #     # Retrieve timestamps and calculate stats
    #     stats = queryStats(db, job_id)
        
    #     # Determine job status based on counts and stats
    #     if stats['start_time'] == 0:
    #         status = "not started"
    #     elif stats['end_time'] == 0:
    #         status = "processing"
    #     else:
    #         status = "completed"
        
    #     # Construct the response
    #     response = {
    #         "job_id": job_id,
    #         "status": status,
    #         "counts": count_data.to_dict(),
    #         "stats": {
    #             "start_time": stats['start_time'],
    #             "end_time": stats['end_time'],
    #             "total_time": stats['total_time'],
    #             "average_time": stats['average_time']
    #         }
    #     }
    #     return jsonify(response), 200

    # except Exception as e:
    #     return jsonify({"error": "Failed to retrieve job status", "details": str(e)}), 500



if __name__ == '__main__':
    app.run()