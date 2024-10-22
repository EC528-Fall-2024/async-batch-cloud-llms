from flask import Flask, request, jsonify
import uuid
import time
from functools import wraps

app = Flask(__name__)

# This should be a secure, randomly generated key in a real application
API_KEY = "your-secret-api-key"


# Wrapper for checking if API request has secret API key
def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.headers.get('API-Key') and request.headers.get('X-API-Key') == API_KEY:
            return f(*args, **kwargs)
        else:
            return jsonify({"error": "Invalid or missing API key"}), 401
    return decorated_function


# Function for checking if job_data is valid
def check_valid_job(job_data):
    if job_data is not None:
        return True
    else:
        return False


# Function for posting the new job to the jobs Redis Datastore
def post_job(job_data, job_id):
    pass


# Function for calling batch processor to start job
def notify_batch_processor(job_id):



# Route for submitting a new job
@app.route('/submit_job', methods=['POST'])
@require_api_key
def submit_job():
    job_data = request.json
    if (check_valid_job(job_data)):
        # If valid, generate job ID, post job, and notify batch processor
        job_id = str(uuid.uuid4())
        post_job(job_data, job_id)
        notify_batch_processor(job_id)
        return jsonify({"job_id": job_id, "status": "submitted"})
    else:
        return 

@app.route('/job_status/<job_id>', methods=['GET'])
@require_api_key
def job_status(job_id):
    job = jobs.get(job_id)
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
    app.run(debug=True)