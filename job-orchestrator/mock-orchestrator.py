######
######
# This is a mock job orchestrator.
# It will listen to pub/sub messages. On a pub/sub message, it will call the batch processor 
# The contents of the Pub/Sub message are NOT the body of the contents of the Batch Processor Request 
# They are completely different.

# Developed by Noah Robitshek Nov 18th, 2024
#####
#####

from google.cloud import pubsub_v1
import time
import requests
import json
from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1


## Project Settings
project_id = "elated-scope-437703-h9"
subscription_id = "IncomingJob-sub"
# subscription_id = "IncomingJob-sub"
# subscription_id = "ProgressLogs-sub"


# CHANGE 
# LocalHost
url = "http://127.0.0.1:8080"

# Cloud Deployed
# url = "https://us-central1-elated-scope-437703-h9.cloudfunctions.net/batch-processor-http"


timeout = 200.0

subscriber = pubsub_v1.SubscriberClient()
# The `subscription_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/subscriptions/{subscription_id}`
subscription_path = subscriber.subscription_path(project_id, subscription_id)


def call_batch_processor():
    payload = json.dumps({
    "Job_ID": "1",
    "Client_ID": "rick sorkin",
    "User_Project_ID": "sampleproject-440900",
    "User_Dataset_ID": "user_dataset",
    "Input_Table_ID": "input_table",
    "Output_Table_ID": "output_2",
    "Model": "gpt-3.5-turbo",
    "API_key": ""
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
        

def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    print(f"Received {message}.")
    ## Call the API Here
    print("Calling the batch processor now")
    print(call_batch_processor())
    message.ack()


streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}..\n")

# Wrap subscriber in a 'with' block to automatically call close() when done.
with subscriber:
    try:
        # When `timeout` is not set, result() will block indefinitely,
        # unless an exception is encountered first.
        streaming_pull_future.result(timeout=timeout)
    except TimeoutError:
        streaming_pull_future.cancel()  # Trigger the shutdown.
        streaming_pull_future.result()  # Block until the shutdown is complete.