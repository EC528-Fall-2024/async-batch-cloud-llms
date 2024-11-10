from google.cloud import pubsub_v1
from BigQueryWriter import write_response
import threading

############ FOR CLOUD DEPLOYMENT ################
from flask import Flask
import threading

app = Flask(__name__)

@app.route("/")
def health_check():
    return "Running", 200

def run_flask():
    app.run(host="0.0.0.0", port=8080)

##################### REVERSE BATCH PROCESSOR ###################
project_id = "elated-scope-437703-h9"
subscription_id = "OutputData-sub"

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    # Decode the data from bytes to string
    data = message.data.decode("utf-8")
    
    # Extract attributes from the message
    job_id = message.attributes.get("Job_ID")
    client_id = message.attributes.get("Client_ID")
    row_number = message.attributes.get("Row_Number")

    # Print received message and attributes
    print(f"Received message: {data}")
    print(f"Job_ID: {job_id}")
    print(f"Client_ID: {client_id}")
    print(f"Row_Number: {row_number}")

    # Acknowledge the message
    message.ack()
    
    # Write the message to a database
    write_response(row_number, data)

# Start Flask server to start rate limiter in cloud
threading.Thread(target=run_flask).start()

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}..\n")

with subscriber:
    try:
        streaming_pull_future.result()
    except:
        streaming_pull_future.cancel()  # Trigger the shutdown