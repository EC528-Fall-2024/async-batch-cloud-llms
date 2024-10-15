# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app/API

# Copy the current directory contents into the container at /app/API
COPY . /app/API

RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 5000


ENV FLASK_APP=app.py


CMD ["python", "app.py"]
