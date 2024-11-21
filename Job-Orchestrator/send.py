from google.cloud import pubsub_v1

def pubSubSender(message):
    project_id = "elated-scope-437703-h9"
    topic_id = "IncomingJob"

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    message_str = f"{message}"
    message = message_str.encode("utf-8")
    
    # Define attributes as a dictionary
    attributes = {
        "Job_ID": "2",
        "Client_ID": "Rick Sorkin",
        "User_Project_ID": "sampleproject-440900",
        "User_Dataset_ID": "user_dataset",
        "Input_Table_ID": "input_table",
        'Output_Table_ID': "output_2",
        'Model': "gpt-3.5-turbo",
        'API_key': ""
    }

    future = publisher.publish(topic_path, message, **attributes)
    print(future.result())

# Example usage
if __name__ == "__main__":
    data = "IncomingJob"
    pubSubSender(data)