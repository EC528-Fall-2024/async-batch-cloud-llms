from google.cloud import pubsub_v1

def pubSubSender(message):
    project_id = "elated-scope-437703-h9"
    
    # CHANGE FOR INPUT/OUTPUT
    # topic_id = "InputData"
    topic_id = "OutputData"


    publisher = pubsub_v1.PublisherClient()
    # The `topic_path` method creates a fully qualified identifier
    # in the form `projects/{project_id}/topics/{topic_id}`
    topic_path = publisher.topic_path(project_id, topic_id)

    data_str = f"{message}"
    # Data must be a bytestring
    data = data_str.encode("utf-8")
    
        # Define attributes as a dictionary
    attributes = {
        "Job_ID": "wolf",
        "Client_ID": "richard",
        "Row_Number": "15"
    }

    # Pass the attributes to the publish method
    future = publisher.publish(topic_path, data, **attributes)
    
    print(future.result())
    print("done")

    

# Example usage
if __name__ == "__main__":
    # data = "Sample Article"
    data = "Sample Response"

    pubSubSender(data)