from google.cloud import pubsub_v1
import json

def pubSubSender():
    project_id = "elated-scope-437703-h9"
    
    # CHANGE FOR INPUT/OUTPUT
    # topic_id = "InputData"
    # topic_id = "OutputData"
    # topic_id = "StartJob"
    topic_id = "IncomingJob"

    data = {
        "Table_Key": "json_key",
        "Project_ID": "Example_Project_ID",
        "Dataset_ID": "Example_Dataset_ID",
        "Table_ID": "Input_Table_ID",
        "LLM_Model": "GTP-3.5" ,
        "Row_Count": "int_example",
        "prompt_prefix": "Example prompt to add in front of request body",
        "prompt_postfix": "Example prompt to add in after request body",
        "Request_Column": "int_example",
        "Response_Column": "int_example"
    }

    json_data = json.dumps(data)
    encoded_data = json_data.encode('utf-8')

    publisher = pubsub_v1.PublisherClient()
    # The `topic_path` method creates a fully qualified identifier
    # in the form `projects/{project_id}/topics/{topic_id}`
    topic_path = publisher.topic_path(project_id, topic_id)

    attributes = {
        "Job_ID": "1",
        "Client_ID": "rick sorkin",
    }
    
    # Pass the attributes to the publish method
    future = publisher.publish(topic_path, encoded_data, **attributes)
    
    print(future.result())
    print("done")

    

# Example usage
if __name__ == "__main__":
    
    # data = "Sample Article"
    pubSubSender()