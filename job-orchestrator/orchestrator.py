from sqlalchemy import text
import json
import os
from google.cloud.sql.connector import Connector, IPTypes
import sqlalchemy


# initialize Connector object
connector = Connector()


# function to return the database connection object
def getconn():
    conn = connector.connect(
        "elated-scope-437703-h9:us-east5:job-orchestration-database",
        "pg8000",
        user="orchestrator",
        password="m~o'I39?A@8cu?;P",
        db="job-orchestration-database"
    )
    return conn


# create connection pool with 'creator' argument to our connection object function
pool = sqlalchemy.create_engine(
    "postgresql+pg8000://",
    creator=getconn,
)


# Function for creating the jobs table
def create_table():
    with pool.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS jobs (
                job_id VARCHAR(255) PRIMARY KEY,
                client_id VARCHAR(255),
                is_valid BOOLEAN NOT NULL DEFAULT TRUE,
                in_progress BOOLEAN NOT NULL DEFAULT FALSE,
                is_completed BOOLEAN NOT NULL DEFAULT FALSE,
                rows_processed INTEGER NOT NULL DEFAULT 0,
                row_count INTEGER NOT NULL DEFAULT 0,
                table_key JSON,
                table_id VARCHAR(255),
                project_id VARCHAR(255),
                table_id VARCHAR(255),
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
def insert_job(job_data):
    with pool.connect() as conn:
        conn.execute(text("""
            INSERT INTO jobs (
                job_id,
                client_id,
                table_key,
                project_id,
                dataset_id,
                table_id,
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
def update_job(job_id, **kwargs):
    updates = []
    parameters = {"job_id": job_id}
    for key, value in kwargs.items():
        if value is not None:
            updates.append(f"{key} = :{key}")
            parameters[key] = value
    with pool.connect() as conn:
        if updates:  # Proceed only if there are updates to be made
            conn.execute(text(f"""
                UPDATE jobs
                SET {', '.join(updates)}, updated_at = CURRENT_TIMESTAMP
                WHERE job_id = :job_id
            """), parameters)
            conn.commit()


# Function for reading all job data
def read_job(job_id):
    with pool.connect() as conn:
        result = conn.execute(text("""
            SELECT *
            FROM jobs
            WHERE job_id = :job_id
        """), {"job_id": job_id})
        return result.fetchone()


# Main function
def main():
    try:
        # Connect to the database and create the table
        create_table()
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
        insert_job(fake_job_data)
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


if __name__ == "__main__":
    main()