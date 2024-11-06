from flask import Flask, request, jsonify
import uuid
import time
import json
import os
import requests
from google.cloud import pubsub_v1
from flask_cors import CORS

# Batch Processor URL
BATCH_PROCESSOR_URL = "https://0e3b-128-197-28-149.ngrok-free.app"

app = Flask(__name__)
CORS(app)

app.config['DEBUG'] = os.environ.get('FLASK_DEBUG')


# Set up pub/sub publisher for IncomingJob topic
project_id = "elated-scope-437703-h9"
topic_id = "IncomingJob"

publisher = pubsub_v1.PublisherClient()
# The `topic_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/topics/{topic_id}`
topic_path = publisher.topic_path(project_id, topic_id)


# Function for submitting job
def publish_job(job_data, job_id): 
    # Activate batch processor
    headers = {
        "Content-Type": "application/json",
    }
    job_message = {
        "Job_ID": job_id,
        "Client_ID": job_data["client_id"],
        "Database_Length": job_data["row_count"]
    }
    response = requests.post(f"{BATCH_PROCESSOR_URL}/go", json=job_message, headers=headers)

    data_str = {
        "job_id": job_id,
        "client_id": job_data["client_id"],
        "project_id": job_data["project_id"],
        "dataset_id": job_data["dataset_id"],
        "table_id": job_data["table_id"],
        "table_key": job_data["table_key"],
        "row_count": job_data["row_count"],
        "request_column": job_data["request_column"],
        "response_column": job_data["response_column"],
        "llm_model": job_data["llm_model"],
        "prompt_prefix": job_data["prompt_prefix"],
        "prompt_postfix": job_data["prompt_postfix"]
    }
    # Data must be a bytestring
    json_data = json.dumps(data_str)
    encoded_data = json_data.encode('utf-8')
    
    # Define attributes as a dictionary
    attributes = {
        "job_id": "job_id",
        "client_id": job_data["client_id"]
    }

    # Pass the attributes to the publish method
    future = publisher.publish(topic_path, encoded_data, **attributes)
    
    print(future.result())
    print(response.json())


# Function for checking if job_data is valid
def check_valid_job(job_data):
    if job_data is not None:
        return True
    else:
        return False


# Route for submitting a new job
@app.route('/submit_job', methods=['POST'])
def submit_job():
    job_data = request.json
    if (check_valid_job(job_data)):
        # If valid, generate job ID, post job, and notify batch processor
        job_id = str(uuid.uuid4())
        publish_job(job_data, job_id)

        # Return job ID to user and indicate that job is submitted
        return jsonify({"job_id": job_id, "status": "submitted"})
    else:
        # Job was not valid
        return jsonify({"error": "Job not valid"}), 400


# Route for checking 
@app.route('/job_status/<job_id>', methods=['GET'])
def job_status(job_id):
    job = None
    if (job is None):
        return jsonify({"error": "Job not found"}), 404
    if job:
        # Simulate job progress
        elapsed_time = time.time() - job['created_at']
        if elapsed_time > 30:
            job['status'] = "completed"
        elif elapsed_time > 10:
            job['status'] = "processing"
        
        return jsonify({
            "job_id": job_id,
            "status": job['status'],
            "data": job['data']
        })
    else:
        return jsonify({"error": "Job not found"}), 404


if __name__ == '__main__':
    app.run()