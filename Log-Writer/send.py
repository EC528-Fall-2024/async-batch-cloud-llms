from google.cloud import pubsub_v1

def pubSubSender(message):
    project_id = "elated-scope-437703-h9"
    topic_id = "Logs"

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    message_str = f"{message}"
    message = message_str.encode("utf-8")
    
    # Define attributes as a dictionary
    attributes = {
        "Job_ID": "1",
        "Log_Type": "Progress",
        "Client_ID": "Rick Sorkin",
        "Microservice": "RateLimiter",
        "Row_Number": "1",
        "Num_Rows": "10",
        "Error_Type": ""
    }

    future = publisher.publish(topic_path, message, **attributes)
    print(future.result())

# Example usage
if __name__ == "__main__":
    data = "test"
    pubSubSender(data)