from google.cloud import pubsub_v1 

# Send message to Rate-Limtier via InputData Pub/Sub topic
def pubSubSender(row, message, Job_ID, Client_ID):
    project_id = "elated-scope-437703-h9"
    topic_id = "InputData"

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    data = f"{message}".encode("utf-8")
    
        # Define attributes as a dictionary
    attributes = {
        "Job_ID": str(Job_ID),
        "Client_ID": str(Client_ID),
        "Row_Number": str(row)
    }

    # Send message to rate limiter
    publisher.publish(topic_path, data, **attributes)