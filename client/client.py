from google.cloud import pubsub_v1
from datasets import load_dataset
from tqdm import tqdm
import json
import uuid
import threading

# Load the news articles **crawled** in the year 2016 (but not necessarily published in 2016), in streaming mode
dataset = load_dataset("stanford-oval/ccnews", name="2016", streaming=True)

# Google cloud sub/pub system configuration
project_id = "your-project-id"
input_topic_id = "inbound-data"
output_topic_id = "outbound-data"

# Set up publisher
publisher = pubsub_v1.PublisherClient()
input_topic_path = publisher.topic_path(project_id, input_topic_id)

# Set up subscriber
subscriber = pubsub_v1.SubscriberClient()
output_topic_path = subscriber.topic_path(project_id, output_topic_id)

# Define method for publishing a method to inbound-data topic
def publish_message(client_id, data):
    # Set up message
    message_id = str(uuid.uuid4())
    attributes = {
        'client_id': client_id,
        'message_id': message_id
    }
    message = {
        'id': message_id,
        'data': data
    }
    # Publish message and view result
    future = publisher.publish(input_topic_path, json.dumps(message).encode('utf-8'), **attributes)
    future.result()
    print(f"Published message {message_id} for client {client_id}")

# Define method for creating filtered subscription path
def create_filtered_subscription(client_id):
    subscription_id = f"client-{client_id}-sub"
    subscription_path = subscriber.subscription_path(project_id, subscription_id)
    
    filter_string = f'attributes.client_id = "{client_id}"'
    
    with subscriber:
        subscription = subscriber.create_subscription(
            request={
                "name": subscription_path,
                "topic": output_topic_path,
                "filter": filter_string
            }
        )
    return subscription_path

# Callback for subscription response message
def process_response(message):
    response = json.loads(message.data.decode("utf-8"))
    print(f"Received processed data: {response}")
    message.ack()

# Script for getting client subscription results
def listen_for_responses(client_id):
    subscription_path = create_filtered_subscription(client_id)
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=process_response)
    with subscriber:
        try:
            streaming_pull_future.result()
        except TimeoutError:
            streaming_pull_future.cancel()
            streaming_pull_future.result()


def client_stream(client_id):
    # Start listening for responses in a separate thread for each client
    threading.Thread(target=listen_for_responses, args=(client_id,), daemon=True).start()

    # Simulate streaming data
    for i, example in enumerate(dataset["train"].take(5)):
        data = "Return a json file containing the sentiment analysis of this article:\n" + str(example['plain_text'])
        publish_message(client_id, data)

# Simulate multiple clients
client_ids = ['client1', 'client2', 'client3']
threads = []
for client_id in client_ids:
    thread = threading.Thread(target=client_stream, args=(client_id,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()


