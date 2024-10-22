# Use a lightweight Python image
FROM python:3.9-slim

# Install Redis server
RUN apt-get update && apt-get install -y redis

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code into the container
COPY . .

# Expose Redis port for local testing (not necessary for Cloud Run)
EXPOSE 6379

# Start Redis in the background and then run your Python script
CMD redis-server --daemonize yes && python dynamic_token_bucket.py
