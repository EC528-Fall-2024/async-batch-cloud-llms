from google.cloud import pubsub_v1 

project_id = "elated-scope-437703-h9"
input_topic = "InputData"
stats_topic = "Stats"


# Send message to Rate-Limtier via InputData Pub/Sub topic
def pubSubSender(row:int, message:str, Job_ID:str, Client_ID:str, User_Project_ID:str, User_Dataset_ID:str, Output_Table_ID:str, Model:str, API_key:str, Job_Length:int):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, input_topic)
    data = f"{message}".encode("utf-8")
    
    # Define attributes as a dictionary
    # Not sure if we need string casting....
    attributes = {
        "API_key": str(API_key),
        "Client_ID": str(Client_ID),
        "Job_ID": str(Job_ID),
        "Job_Length": str(Job_Length),
        "Model": str(Model),
        "Output_Table_ID": str(Output_Table_ID),
        "Row_Number": str(row),
        "User_Dataset_ID": str(User_Dataset_ID),
        "User_Project_ID": str(User_Project_ID),
    }

    # Send message to rate limiter
    publisher.publish(topic_path, data, **attributes)

# send time metrics to status collector
def send_metrics(client_id, job_id, row, start):
    publisher = pubsub_v1.PublisherClient()
    publisher_path = publisher.topic_path(project_id, stats_topic)

    # Prepare message to publish
    service = "BatchProcessor"
    message = service.encode("utf-8")
    attributes = {
        "Job_ID": f"{job_id}",
        "Client_ID": f"{client_id}",
        "Row": f"{row}",
        "Start": str(start),
        "In_LLM": "",
        "Out_LLM": "",
        "End": ""
    }

    # Send out response via pub/sub
    publisher.publish(publisher_path, message, **attributes)
    print("Sent time metrics to stats collector") 