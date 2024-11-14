'''Send Messages to Reverse Batch Processor'''
from google.cloud import pubsub_v1

# Project information
project_id = "elated-scope-437703-h9"
output_topic = "OutputData"

# send message to reverse batch processor
def send_response(client_id, job_id, row, response):
    publisher = pubsub_v1.PublisherClient()
    publisher_path = publisher.topic_path(project_id, output_topic)

    # Prepare message to publish
    message = response.encode("utf-8")
    attributes = {
        "Job_ID": f"{job_id}",
        "Client_ID": f"{client_id}",
        "Row_Number": f"{row}"
    }

    # Send out response via pub/sub
    publisher.publish(publisher_path, message, **attributes)
    print("Sent response to reverse batch processor") 