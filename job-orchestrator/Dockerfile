# Use a base image that includes Python
FROM python:3.11.6

# Set the working directory in the container
WORKDIR /app

ENV DB_USER="orchestrator"
ENV DB_PASS="'<PhKBLqY{[p:b3b"
ENV DB_NAME="jobs"
ENV INSTANCE_CONNECTION_NAME="elated-scope-437703-h9:us-east5:job-orchestration-database"
ENV PROJECT_ID="elated-scope-437703-h9"

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set the command to run the application
CMD ["python", "orchestrator.py"]