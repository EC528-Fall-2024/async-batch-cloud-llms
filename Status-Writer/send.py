from google.cloud import pubsub_v1

def pubSubSender(message):
    project_id = "elated-scope-437703-h9"
    topic_id = "Status"

    publisher = pubsub_v1.PublisherClient()
    # The `topic_path` method creates a fully qualified identifier
    # in the form `projects/{project_id}/topics/{topic_id}`
    topic_path = publisher.topic_path(project_id, topic_id)

    message_str = f"{message}"
    # Data must be a bytestring
    message = message_str.encode("utf-8")
    
    # Define attributes as a dictionary
    attributes = {
        "Log_Type": "Error",
        "Microservice": "RateLimiter",
        "Job_ID": "466f47f2-6a5e-4ee1-9603-661095296532",
        "Client_ID": "rayan syed",
        "Row_Number": "3",
        "Num_Rows": "",
        "Error_Type": "RowDropped"
    }

    # Pass the attributes to the publish method
    future = publisher.publish(topic_path, message, **attributes)
    
    print(future.result())
    print("done")

# Example usage
if __name__ == "__main__":
    data = "Solve: 1+1"
    pubSubSender(data)