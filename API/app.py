from confluent_kafka import Producer, Consumer, KafkaException, KafkaError
from flask import Flask, request, jsonify
import pandas as pd
import json
import threading
import os
import requests
import socket
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

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

# Kafka configurations
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "llm_requests")
KAFKA_SERVER = os.getenv("KAFKA_SERVER", "localhost:9092")
KAFKA_GROUP_ID = os.getenv("KAFKA_GROUP_ID", "llm_group")

# Initialize Kafka producer with confluent-kafka
producer_config = {
    'bootstrap.servers': KAFKA_SERVER,
    'client.id': socket.gethostname()
}
producer = Producer(producer_config)

# Producer delivery report callback function
def acked(err, msg):
    """Delivery report callback for Kafka producer."""
    if err:
        logging.error(f"Failed to deliver message: {msg.value().decode('utf-8')}: {err}")
    else:
        logging.info(f"Message produced: {msg.value().decode('utf-8')}")

@app.route('/process', methods=['POST'])
def process_file():
    """API endpoint to accept a prompt and optionally a CSV file, then queue it in Kafka."""
    
    # Get the prompt from the form data
    prompt = request.form.get('prompt')
    
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    # Get the uploaded CSV file (optional)
    file = request.files.get('file')

    # If a file is provided, process it
    if file:
        # Read the CSV file into a pandas DataFrame
        try:
            df = pd.read_csv(file)
            # Convert the DataFrame into a string format
            data_str = df.to_csv(index=False)
        except Exception as e:
            return jsonify({"error": f"Error reading CSV file: {str(e)}"}), 400
    else:
        # If no file is provided, set data_str to an empty string or a placeholder
        data_str = "No file provided"

    # Construct the message payload with both prompt and (optional) CSV data
    message = {
        "prompt": prompt,
        "data": data_str
    }

    # Send the message to the Kafka topic
    try:
        producer.produce(KAFKA_TOPIC, key=message['prompt'], value=json.dumps(message).encode('utf-8'), callback=acked)
        producer.poll(0)  # Trigger delivery report callbacks
        producer.flush()  # Ensure the message is actually sent
    except Exception as e:
        return jsonify({"error": f"Failed to send message to Kafka: {str(e)}"}), 500

    # Respond with a success message
    return jsonify({"message": "Data successfully queued in Kafka"}), 200

def send_to_openai(prompt, data):
    """Send a request to OpenAI using HTTP request with Authorization header."""
    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {openai_api_key}",
        "Content-Type": "application/json"
    }

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
    """Kafka consumer to listen for messages and send them to an LLM."""
    consumer_config = {
        'bootstrap.servers': KAFKA_SERVER,
        'group.id': KAFKA_GROUP_ID,
        'auto.offset.reset': 'earliest'
    }

    consumer = Consumer(consumer_config)
    consumer.subscribe([KAFKA_TOPIC])

    while True:
        msg = consumer.poll(timeout=1.0)

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                logging.error(f"Kafka error: {msg.error()}")
                break

        msg_data = json.loads(msg.value().decode('utf-8'))
        prompt = msg_data['prompt']
        data = msg_data['data']

        full_prompt = f"{prompt}\n\nHere is the data:\n{data}"

        try:
            response = send_to_openai(full_prompt, data)
            logging.info(f"LLM Response: {response['choices'][0]['message']['content']}")
        except Exception as e:
            logging.error(f"Failed to process LLM request: {str(e)}")

# Start Kafka consumer in a separate thread
def start_kafka_consumer():
    """Start the Kafka consumer thread."""
    consumer_thread = threading.Thread(target=consume_from_kafka)
    consumer_thread.daemon = True  # This ensures the thread exits when the main program does
    consumer_thread.start()

if __name__ == '__main__':
    # Start the Kafka consumer in a separate thread
    start_kafka_consumer()

    # Run the Flask app
    app.run(debug=True)
