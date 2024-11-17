from google.cloud import pubsub_v1

def pubSubSender(message):
    project_id = "elated-scope-437703-h9"
    topic_id = "InputData"

    publisher = pubsub_v1.PublisherClient()
    # The `topic_path` method creates a fully qualified identifier
    # in the form `projects/{project_id}/topics/{topic_id}`
    topic_path = publisher.topic_path(project_id, topic_id)

    message_str = f"{message}"
    # Data must be a bytestring
    message = message_str.encode("utf-8")
    
    # Define attributes as a dictionary
    attributes = {
        "Job_ID": "test",
        "Client_ID": "user1",
        "Row_Number": "1",
        "User_Project_ID": "test",
        "User_Dataset_ID": "test",
        "Job_Length": "1",
        'Output_Table_ID': "test",
        'Model': "gpt-3.5-turbo",
        'API-key': ""
    }

    # Pass the attributes to the publish method
    future = publisher.publish(topic_path, message, **attributes)
    
    print(future.result())
    print("done")

# Example usage
if __name__ == "__main__":
    data = "Solve: 1+1"
    pubSubSender(data)