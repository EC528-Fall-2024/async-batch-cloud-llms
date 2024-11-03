from google.cloud.sql.connector import Connector
import sqlalchemy
from sqlalchemy import text

connector = Connector()


# Set up connection to PostgreSQL job-data database
def getconn():
    return connector.connect(
        "elated-scope-437703-h9:us-east5:job-orchestration-database",
        "pg8000",
        user="postgres",
        password="m~o'I39?A@8cu?;P",
        db="job-data"
    )


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
                llm_model,
                prompt_prefix,
                prompt_postfix
            )
            VALUES (
                :job_id,
                :client_id,
                :table_key,
                :project_id,
                :llm_model,
                :prompt_prefix,
                :prompt_postfix
            )
        """), {
            "job_id": job_data["job_id"],
            "client_id": client_id,
            "table_key": table_key,
            "project_id": project_id,
            "llm_model": llm_model,
            "prompt_prefix": prompt_prefix,
            "prompt_postfix": prompt_postfix
        })
        conn.commit()


# Function for updating 
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

# Example usage
new_data = {"value1": "example", "value2": 123}
write_data(new_data)