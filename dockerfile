# Use an official Python 3.8 slim image as the base image
# The base image contains the OS and essential tools
FROM python:3.8-slim

# Set environment variables to prevent Python from writing .pyc files
# and to ensure output is flushed directly to the terminal (unbuffered output)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies using apt-get
# -y option automatically answers "yes" to prompts
# Clean up unnecessary files to reduce image size
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
# This is where the app code will reside and where the subsequent commands will run
WORKDIR /app

# Copy the current directory contents from the host machine into the container
# Assuming the current directory contains the source code and requirements.txt
COPY . /app

# Install Python dependencies from the requirements.txt file
# --no-cache-dir avoids caching to reduce disk space usage
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the application will run on
# This doesn't open the port, just documents it for future use
EXPOSE 8080

# Specify the command to run when the container starts
# This runs the Python application file `app.py`
CMD ["python", "demo.py"]
