import os
import json
from google.cloud.sql.connector import Connector, IPTypes
import sqlalchemy
from flask import Flask
from google.cloud import pubsub_v1
import threading

app = Flask(__name__)

@app.route('/')
def home():
    main()
    return "Job processing complete", 200

# Environment variables
db_user = os.environ["DB_USER"]
db_pass = os.environ["DB_PASS"]
db_name = os.environ["DB_NAME"]
db_instance_connection_name = os.environ["INSTANCE_CONNECTION_NAME"]
project_id = os.environ["PROJECT_ID"]

# Initialize Connector object
connector = None
pool = None

# Pubsub topic IDs
progress_id = "ProgressLogs-sub"
error_id = "ErrorLogs-sub"
job_topic_id = "IncomingJob"

def init_pool(connector):
    def getconn():
        connection = connector.connect(
            f"{db_instance_connection_name}",
            "pg8000",
            user=db_user,
            password=db_pass,
            db=db_name,
            ip_type=IPTypes.PUBLIC,  #IPTypes.PRIVATE for Private IP
        )
        return connection
    # create connection pool
    engine = sqlalchemy.create_engine("postgresql+pg8000://", creator=getconn)
    return engine


# Function for creating the jobs table
def create_table(pool):
    with pool.connect() as conn:
        conn.execute(sqlalchemy.text("""
            CREATE TABLE IF NOT EXISTS jobs (
                job_id VARCHAR(255) PRIMARY KEY,
                client_id VARCHAR(255),
                is_valid BOOLEAN NOT NULL DEFAULT TRUE,
                in_progress BOOLEAN NOT NULL DEFAULT FALSE,
                is_completed BOOLEAN NOT NULL DEFAULT FALSE,
                rows_processed INTEGER NOT NULL DEFAULT 0,
                row_count INTEGER NOT NULL DEFAULT 0,
                table_key JSON,
                input_table_id VARCHAR(255),
                project_id VARCHAR(255),
                output_table_id VARCHAR(255),
                llm_model VARCHAR(255),
                error_list TEXT[],
                request_column INTEGER NOT NULL DEFAULT 0,
                response_column INTEGER NOT NULL DEFAULT 0,
                prompt_prefix VARCHAR(255),
                prompt_postfix VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))
        conn.commit()


# Function for writing new job to job-data database
def insert_job(pool, job_data):
    with pool.connect() as conn:
        conn.execute(sqlalchemy.text("""
            INSERT INTO jobs (
                job_id,
                client_id,
                table_key,
                project_id,
                dataset_id,
                input_table_id,
                output_table_id,
                row_count,
                request_column,
                response_column,
                llm_model,
                prompt_prefix,
                prompt_postfix
            )
            VALUES (
                :job_id,
                :client_id,
                :table_key,
                :project_id,
                :dataset_id,
                :table_id,
                :row_count,
                :request_column,
                :response_column,
                :llm_model,
                :prompt_prefix,
                :prompt_postfix
            )
        """), {
            "job_id": job_data["job_id"],
            "client_id": job_data["client_id"],
            "table_key": job_data["table_key"],
            "project_id": job_data["project_id"],
            "dataset_id": job_data["dataset_id"],
            "table_id": job_data["table_id"],
            "row_count": job_data["row_count"],
            "request_column": job_data["request_column"],
            "response_column": job_data["response_column"],
            "llm_model": job_data["llm_model"],
            "prompt_prefix": job_data["prompt_prefix"],
            "prompt_postfix": job_data["prompt_postfix"]
        })
        conn.commit()


# Function for updating job with specified job_id
def update_job(pool, job_id, **kwargs):
    updates = []
    parameters = {"job_id": job_id}
    for key, value in kwargs.items():
        if value is not None:
            updates.append(f"{key} = :{key}")
            parameters[key] = value
    with pool.connect() as conn:
        if updates:  # Proceed only if there are updates to be made
            conn.execute(sqlalchemy.text(f"""
                UPDATE jobs
                SET {', '.join(updates)}, updated_at = CURRENT_TIMESTAMP
                WHERE job_id = :job_id
            """), parameters)
            conn.commit()


# Function for reading all job data
def read_job(pool, job_id):
    with pool.connect() as conn:
        result = conn.execute(sqlalchemy.text("""
            SELECT *
            FROM jobs
            WHERE job_id = :job_id
        """), {"job_id": job_id})
        return result.fetchone()


# Main function
def main():
    try:
        global connector, pool
        if not pool:
            connector = Connector()
            pool = init_pool(connector)
        # Connect to the database and create the table
        create_table(pool)
        print("Table created successfully.")

        # Create fake job data
        fake_job_data = {
            "job_id": "18cbe750-edba-4537-ad24-9c0a0a163c4f",
            "client_id": "client_123",
            "table_key": json.dumps({"key1": "value1", "key2": "value2"}),
            "project_id": "project_456",
            "dataset_id": "dataset_789",
            "table_id": "table_101112",
            "row_count": 1000,
            "request_column": 0,
            "response_column": 1,
            "llm_model": "gpt-3.5",
            "prompt_prefix": "Translate the following to French:",
            "prompt_postfix": "Ensure the translation is grammatically correct."
        }

        # Insert the fake job data
        insert_job(pool, fake_job_data)
        print(f"Job inserted successfully with ID: {fake_job_data['job_id']}")

        # Read the inserted job data
        job = read_job(fake_job_data['job_id'])
        if job:
            print("\nRetrieved job data:")
            for column, value in job._mapping.items():
                print(f"{column}: {value}")
        else:
            print("Job not found.")

    except Exception as e:
        print(f"An error occurred: {e}")


def error(message):
    print(f"Received error message: {message}")
    message.ack()


def error_subscribe():
    subscriber = pubsub_v1.SubscriberClient()
    error_path = subscriber.subscription_path(project_id, error_id)
    streaming_pull_future = subscriber.subscribe(f"{error_path}", callback=error)
    print(f"Listening for messages on {error_path}..\n")
    with subscriber:
        try:
            streaming_pull_future.result()
        except:
            streaming_pull_future.cancel() 


def progress(message):
    print(f"Received progress message: {message}")
    message.ack()


def progress_subscribe():
    subscriber = pubsub_v1.SubscriberClient()
    progress_path = subscriber.subscription_path(project_id, progress_id)
    streaming_pull_future = subscriber.subscribe(f"{progress_path}", callback=progress)
    print(f"Listening for messages on {progress_path}..\n")
    with subscriber:
        try:
            streaming_pull_future.result()
        except:
            streaming_pull_future.cancel() 


def job():
    pass


def job_subscribe():
    subscriber = pubsub_v1.SubscriberClient()
    job_path = subscriber.subscription_path(project_id, job_topic_id)
    streaming_pull_future = subscriber.subscribe(f"{job_path}", callback=job)
    print(f"Listening for messages on {job_path}..\n")
    with subscriber:
        try:
            streaming_pull_future.result()
        except:
            streaming_pull_future.cancel() 


if __name__ == "__main__":
    threading.Thread(target=progress_subscribe).start()
    threading.Thread(target=error_subscribe).start()
    threading.Thread(target=job_subscribe).start()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
    main()