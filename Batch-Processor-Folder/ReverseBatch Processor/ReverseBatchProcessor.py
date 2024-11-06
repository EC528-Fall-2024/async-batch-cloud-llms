from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1
from BigQueryWriter import write_response

project_id = "elated-scope-437703-h9"
subscription_id = "OutputData-sub"
timeout = 3000.0

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


streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}..\n")

with subscriber:
    try:
        # When `timeout` is not set, result() will block indefinitely,
        # unless an exception is encountered first.
        streaming_pull_future.result(timeout=timeout)
    except TimeoutError:
        streaming_pull_future.cancel()  # Trigger the shutdown.
        streaming_pull_future.result()  # Block until the shutdown is complete.