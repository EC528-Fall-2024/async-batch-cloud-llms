'''Continuously Receive Messages from Reverse Batch Processor'''
from google.cloud import pubsub_v1
from RateLimiter import rate_limit

# Project information
project_id = "elated-scope-437703-h9"
input_topic = "InputData-sub"

# Convert input to batch format
def process_message(message):
    # Process incoming message as a 'batch'
    batch = {
        'client_id': message.attributes['Client_ID'],
        'message': message.data.decode('utf-8'),
        'row': message.attributes['Row_Number'],
        'job_id': message.attributes['Job_ID']
    }
    print("Rate-limiter received message from batch processor.") 

    # Acknowledge message
    message.ack()

    # Process the batch
    rate_limit(batch)
    
def batch_receiver():
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, input_topic)

    # Subscribe to topic with continuous streaming
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=process_message)
    print(f"Listening for messages on {subscription_path}..\n")

    # Keep the main thread alive to allow asynchronous message handling
    try:
        streaming_pull_future.result()
    except:
        print("Streaming pull feature on input topic failed")
        streaming_pull_future.cancel()