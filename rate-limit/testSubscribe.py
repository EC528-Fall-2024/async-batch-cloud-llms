from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1

# TODO(developer)
project_id = "elated-scope-437703-h9"
subscription_id = "InputData-sub"
# Number of seconds the subscriber should listen for messages
timeout = 20.0

subscriber = pubsub_v1.SubscriberClient()
# The `subscription_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/subscriptions/{subscription_id}`
subscription_path = subscriber.subscription_path(project_id, subscription_id)

def callbafrom google.cloud import pubsub_v1
import time

def dequeue_one_message(project_id, subscription_id, timeout=10):
    """
    Pulls one message from a Pub/Sub subscription, processes it, and acknowledges it.

    Args:
    - project_id (str): Google Cloud project ID.
    - subscription_id (str): Pub/Sub subscription ID.
    - timeout (int): Time to wait for a message before timing out.
    """

    # Initialize a subscriber client
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)
    
    # Pull a single message
    response = subscriber.pull(
        request={
            "subscription": subscription_path,
            "max_messages": 1,  # Limit to one message
        },
        timeout=timeout  # Wait up to `timeout` seconds for a message
    )
    
    if response.received_messages:
        message = response.received_messages[0]
        
        # Process the message (print the message data here, customize as needed)
        print(f"Received message: {message.message.data.decode('utf-8')}")
        
        # Acknowledge the message so it won’t be redelivered
        subscriber.acknowledge(
            request={
                "subscription": subscription_path,
                "ack_ids": [message.ack_id]
            }
        )
        print("Message acknowledged.")
    else:
        print("No messages received within the timeout period.")
    
    # Close the subscriber to free up resources
    subscriber.close()

# Example usage:
# Replace with your project ID and subscription ID
# project_id = "elated-scope-437703-h9"
# subscription_id = "InputData-sub"
dequeue_one_message("elated-scope-437703-h9", "InputData-sub")ck(message: pubsub_v1.subscriber.message.Message) -> None:
    print(f"Received {message}.")
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