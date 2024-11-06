from google.cloud import pubsub_v1

def pubSubSender(message, Job_ID, Client_ID, Row_Number):
    project_id = "elated-scope-437703-h9"
    
    topic_id = "OutputData"

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    data_str = f"{message}"
    # Data must be a bytestring
    data = data_str.encode("utf-8")
    
        # Define attributes as a dictionary
    attributes = {
        "Job_ID": str(Job_ID),
        "Client_ID": str(Client_ID),
        "Row_Number": str(Row_Number)
    }

    # Pass the attributes to the publish method
    future = publisher.publish(topic_path, data, **attributes)
    
    print(future.result())