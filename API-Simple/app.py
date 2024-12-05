from flask import Flask, request, jsonify
import uuid
import time
import json
import os
import requests
from google.cloud import pubsub_v1
from flask_cors import CORS
from google.cloud import firestore 

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
        return jsonify({"Job_ID": job_id, "status": "submitted"}), 200
    else:
        # Job was not valid
        return jsonify({"error": "Job not valid"}), 400


# Internal Function added Dec 5th by noah robitshek
# Inputs: Client_ID, Job_ID
# Outputs: True or False
def jobHasErrors(client_id, job_id):
    
    db = firestore.Client()

    # Define the document reference
    doc_ref = db.collection("Clients").document(client_id).collection("Jobs").document(job_id).collection("Job Data").document("Errors")
    
    # Check if the document exists
    return doc_ref.get().exists


def get_progress(job_id, client_id):
    """
    Helper function to retrieve progress data from Firestore.
    """
    db = firestore.Client()
    doc_ref = (
        db.collection("Clients")
        .document(client_id)
        .collection("Jobs")
        .document("Job " + job_id)
        .collection("Job Data")
        .document("Progress")
    )
    doc = doc_ref.get()
    progress_data = doc.to_dict()

    return {
        "current_row": progress_data.get("current_row", 0),
        "total_rows": progress_data.get("total_rows", 0),
    }
   
# external function added on dec 5th by noah robitshek
# getErrorRows
# Inputs: Client_ID, Job_ID
# Outputs: List of Errors
def getErrorRows(Client_ID, Job_ID):
    db = firestore.Client()

    doc_ref = db.collection("Clients").document(Client_ID).collection("Jobs").document(Job_ID).collection("Job Data").document("Errors")
    docs = doc_ref.get()
    data = docs.to_dict()
    error_rows = data["error_rows"]
        
    return error_rows

@app.route('/job_status/<job_id>', methods=['GET'])
@require_api_key
def job_status(job_id):
    """
    Get the status of a job by querying Firestore.
    """
    try:
        # Extract Client ID from the query parameters
        client_id = request.args.get("Client_ID")

        if not client_id:
            return jsonify({"error": "Client ID is required"}), 400

        # Call the helper function to get progress
        progress_data = get_progress(job_id, client_id)

        # Construct the response
        response = {
            "Job_ID": job_id,
            "Client_ID": client_id,
            "current_row": progress_data["current_row"],
            "total_rows": progress_data["total_rows"],
        }
        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": "Failed to retrieve job status", "details": str(e)}), 500



if __name__ == '__main__':
    app.run()