from flask import Flask, request, jsonify
import pandas as pd
from kafka import KafkaProducer, KafkaConsumer
import json
import threading
from openai import OpenAI
import os
import requests

app = Flask(__name__)

# Load OpenAI API key from a file
def load_openai_api_key(filepath):
    """Read the OpenAI API key from a file."""
    try:
        with open(filepath, 'r') as file:
            return file.read().strip()  # Remove any leading/trailing whitespace or newlines
    except Exception as e:
        raise RuntimeError(f"Error loading OpenAI API key from {filepath}: {e}")

# Load the OpenAI API key from 'OPENAI_API_KEY.txt'
OPENAI_API_KEY_FILE = 'OPENAI_API_KEY.txt'
openai_api_key = load_openai_api_key(OPENAI_API_KEY_FILE)

# Optional: You can set organization and project IDs if needed
organization_id = "your-organization-id"  # Replace with your org ID or None
project_id = "your-project-id"  # Replace with your project ID or None

# Kafka configurations
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "llm_requests")
KAFKA_SERVER = os.getenv("KAFKA_SERVER", "localhost:9092")
KAFKA_GROUP_ID = os.getenv("KAFKA_GROUP_ID", "llm_group")

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers=[KAFKA_SERVER],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)


@app.route('/process', methods=['POST'])
def process_file():
    """API endpoint to accept a prompt and CSV file, then queue it in Kafka"""

    # Get the prompt from the form data
    prompt = request.form.get('prompt')
    # Get the uploaded CSV file
    file = request.files.get('file')

    if not prompt or not file:
        return jsonify({"error": "Prompt and CSV file are required"}), 400

    # Read the CSV file into a pandas DataFrame
    try:
        df = pd.read_csv(file)
    except Exception as e:
        return jsonify({"error": f"Error reading CSV file: {str(e)}"}), 400

    # Convert the DataFrame into a string format
    data_str = df.to_csv(index=False)

    # Construct the message payload with both prompt and CSV data
    message = {
        "prompt": prompt,
        "data": data_str
    }

    # Send the message to the Kafka topic
    try:
        producer.send(KAFKA_TOPIC, value=message)
        producer.flush()  # Ensure the message is actually sent
    except Exception as e:
        return jsonify({"error": f"Failed to send message to Kafka: {str(e)}"}), 500

    # Respond with a success message
    return jsonify({"message": "Data successfully queued in Kafka"}), 200


def send_to_openai(prompt, data):
    """Send a request to OpenAI using HTTP request with Authorization header"""
    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {openai_api_key}",
        "Content-Type": "application/json"
    }

    if organization_id:
        headers["OpenAI-Organization"] = organization_id
    if project_id:
        headers["OpenAI-Project"] = project_id

    payload = {
        "model": "gpt-4o-mini",  # Adjust to the model you are using
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"OpenAI API request failed with status {response.status_code}: {response.text}")


def consume_from_kafka():
    """Kafka consumer to listen for messages and send them to an LLM"""

    # Initialize Kafka consumer
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=[KAFKA_SERVER],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id=KAFKA_GROUP_ID,
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    # Start consuming messages from the Kafka topic
    for message in consumer:
        msg_data = message.value
        prompt = msg_data['prompt']
        data = msg_data['data']

        # Combine prompt and data into a single message for the LLM
        full_prompt = f"{prompt}\n\nHere is the data:\n{data}"

        try:
            # Send the prompt to OpenAI via HTTP request
            response = send_to_openai(full_prompt, data)

            # Log or handle the response (e.g., save to a database or send a notification)
            print(f"LLM Response: {response['choices'][0]['message']['content']}")
        except Exception as e:
            print(f"Failed to process LLM request: {str(e)}")


# Start Kafka consumer in a separate thread
def start_kafka_consumer():
    """Start the Kafka consumer thread"""
    consumer_thread = threading.Thread(target=consume_from_kafka)
    consumer_thread.daemon = True  # This ensures the thread exits when the main program does
    consumer_thread.start()


if __name__ == '__main__':
    # Start the Kafka consumer in a separate thread
    start_kafka_consumer()

    # Run the Flask app
    app.run(debug=True)
