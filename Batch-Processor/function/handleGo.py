from BigQueryReader import read_from_database
from google.cloud import pubsub_v1 #used in pub/sub sender

microservice = "BatchProcessor"

# Actions:
# 1. Read the bigQuery table line by line
# 2. Publish messages to pub/sub line my line

#GeneralLogs - Not used
#ProgressLogs
#ErrorLogs

## Progress Format
# Topic: ProgressLogs
# message=f"Prompt and Text for row {row} read successfully."


## Error Logs Format
# Topic: ErrorLogs
##message = f"Error Reading BigQuery for row {row}: {e}."



# Pub/Sub Sender to Logging Topic -> Job Orcastrator
def log_message(message, job_id, client_id, row, topic_id):
    project_id = "elated-scope-437703-h9"
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    message = f"{message}".encode("utf-8")
    
    # Define attributes as a dictionary
    attributes = {
        "Job_ID": f"{job_id}",
        "Client_ID": f"{client_id}",
        "Microservice:": f"{microservice}",
        "Row_Number": f"{row}"
    }

    publisher.publish(topic_path, message, **attributes)
    print(f"Sent {topic_id} message to job orchestrator.")
    

# Pub/Sub sender to Topic InputData - > Rate Limiter
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

    
def handleGo(Job_ID, Client_ID, Database_Length):
    for i in range(1, int(Database_Length) + 1): 
        # Read the database
        rowFromDatabase = read_from_database(i)
        if rowFromDatabase == None:
            message = f"Error Reading BigQuery for row {i}."
            log_message(message,Job_ID,Client_ID, i, "ErrorLogs")
        else: 
            pubSubSender(i,rowFromDatabase,Job_ID, Client_ID)
            message=f"Prompt and Text for row {i} read successfully."
            log_message(message,Job_ID,Client_ID, i, "ProgressLogs")

        
    
    # Return status
    handleStatus = True
    return handleStatus
    
