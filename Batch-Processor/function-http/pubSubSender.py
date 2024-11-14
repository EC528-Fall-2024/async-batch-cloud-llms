from google.cloud import pubsub_v1 


# Hard Coded Messages
Project_ID =  "project_ID"
Database_ID =  "database"
Input_Table_ID =  "Input_table_ID"
Output_Table_ID = "output_table_ID"
Model =  "none"
API-key =  "example_API_key"

# Send message to Rate-Limtier via InputData Pub/Sub topic
def pubSubSender(row, message, Job_ID, Client_ID):
    project_id = "elated-scope-437703-h9"
    topic_id = "InputData"

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    data = f"{message}".encode("utf-8")
    
        # Define attributes as a dictionary
    attributes = {
        "Job_ID": str(Job_ID),
        "Client_ID": str(Client_ID),
        "Row_Number": str(row),
        "Project_ID": Project_ID,
        "Database_ID": Database_ID,
        "Input_Table_ID": Input_Table_ID,
        "Output_Table_ID": Output_Table_ID,
        "Model": Model,
        "API-key": API-key
    }

    # Send message to rate limiter
    publisher.publish(topic_path, data, **attributes)