'''Send Messages to Reverse Batch Processor'''
from google.cloud import pubsub_v1
from RowProgress import incr_rows, del_rows
from logger import progress_message
from performance import decrementRateLimiter, incrementQueue2

# Project information
project_id = "elated-scope-437703-h9"
output_topic = "OutputData"

# send message to reverse batch processor
def send_response(client_id, job_id, job_length, row, response, user_project_id, user_dataset_id, output_table_id):
    publisher = pubsub_v1.PublisherClient()
    publisher_path = publisher.topic_path(project_id, output_topic)

    # Prepare message to publish
    message = response.encode("utf-8")
    attributes = {
        "Job_ID": f"{job_id}",
        "Client_ID": f"{client_id}",
        "Row_Number": f"{row}",
        "User_Project_ID": f"{user_project_id}",
        "User_Dataset_ID": f"{user_dataset_id}",
	    "Output_Table_ID": f"{output_table_id}"
    }

    # Send out response via pub/sub
    publisher.publish(publisher_path, message, **attributes)
    print("Sent response to reverse batch processor") 

    # Increment Output Queue, Decrement Rate Limiter for Performance Metrics
    try:
        incrementQueue2(job_id)
        decrementRateLimiter(job_id)
    except Exception as e:
        print(f"Error updating performance metrics: {e}...")

    # Update rows 
    processed_rows = incr_rows(job_id)
    if processed_rows is None:
        print(f"Error updating processed rows for job {job_id}")
    else:
        message = f"{processed_rows} rows processed out of {job_length} rows for job {job_id}"
        if processed_rows >= job_length:
            if del_rows(job_id):
                print(f"Job {job_id} data deleted since all rows processed")
            else:
                print(f"Error deleting job {job_id} data")
            message += "... All done"
        print(message)
        progress_message(message, job_id, client_id, processed_rows)