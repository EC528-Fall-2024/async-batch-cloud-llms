from BigQueryReader import read_from_database
from google.cloud import pubsub_v1 #used in pub/sub sender


# Actions:
# 1. Read the bigQuery table line by line
# 2. Publish messages to pub/sub line my line
def handleGo(Job_ID, Client_ID, Database_Length):
    for i in range(1, int(Database_Length) + 1): 
        # Read the database
        rowFromDatabase = read_from_database(i)
        pubSubSender(i,rowFromDatabase,Job_ID, Client_ID)
    
    # Return status
    handleStatus = True
    return handleStatus
    

def pubSubSender(row, message, Job_ID, Client_ID):
    project_id = "elated-scope-437703-h9"
    topic_id = "InputData"

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    data_str = f"{message}"
    data = data_str.encode("utf-8")
    
        # Define attributes as a dictionary
    attributes = {
        "Job_ID": str(Job_ID),
        "Client_ID": str(Client_ID),
        "Row_Number": str(row)
    }

    # Pass the attributes to the publish method
    future = publisher.publish(topic_path, data, **attributes)
    
    print("//////////////////")
    print(future.result())
    print("Message published to Pub/Sub")
    print("The Topic is: " + topic_id)
    # print("The Data is: " + f"{message}")

    