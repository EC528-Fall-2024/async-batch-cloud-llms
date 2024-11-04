from google.cloud import pubsub_v1
import time


# Pulls one message from a Pub/Sub subscription, processes it, and acknowledges it.
def dequeue_one_message(project_id, subscription_id, timeout=2):
    
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
        print(message)
        
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


if __name__ == "__main__":
    dequeue_one_message("elated-scope-437703-h9", "OutputData-sub")