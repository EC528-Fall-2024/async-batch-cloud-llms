FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container
COPY . .

# Expose port 8080 (the port that Cloud Run listens on)
EXPOSE 8080

# Command to run the application
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]

