from google.cloud import pubsub_v1

def pubSubSender():
    project_id = "elated-scope-437703-h9"
    topic_id = "Stats"

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    message_str = "ReverseBatchProcessor"
    # Data must be a bytestring
    message = message_str.encode("utf-8")
    
    # Define attributes as a dictionary
    attributes = {
        "Job_ID": "466f47f2-6a5e-4ee1-9603-661095296532",
        "Client_ID": "rayan syed",
        "Row": "1",
        "Start": "3",
        "In_LLM": "5",
        "Out_LLM": "7",
        "End": "9"
    }

    # Pass the attributes to the publish method
    future = publisher.publish(topic_path, message, **attributes)
    
    print(future.result())
    print("done")

# Example usage
if __name__ == "__main__":
    pubSubSender()