from BigQueryReader import read_from_database

from google.cloud import pubsub_v1 #used in pub/sub sender


# This function will handle the endpoints for go

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
    # The `topic_path` method creates a fully qualified identifier
    # in the form `projects/{project_id}/topics/{topic_id}`
    topic_path = publisher.topic_path(project_id, topic_id)

    data_str = f"{message}"
    # Data must be a bytestring
    data = data_str.encode("utf-8")
    
        # Define attributes as a dictionary
    attributes = {
        "Job_ID": str(Job_ID),
        "Client_ID": str(Client_ID),
        "Row_Number": str(row)
    }

    # Pass the attributes to the publish method
    future = publisher.publish(topic_path, data, **attributes)
    
    print(future.result())
    print("Message published to Pub/Sub")
    

if __name__ == "__main__":
    handleGo('job_1', 'client_1', 13)