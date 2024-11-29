import pytz


#####################
# Operator Notebook #
#####################

## getAllClients
# Inputs: Null
# Outputs: Array of all Clients
def getAllClients(db):
    doc_ref = db.collection("Clients")
    docs = doc_ref.get()
    document_ids = [doc.id for doc in docs]  # Use `doc.id` to get the document ID
    return document_ids


## getAllInfoAboutClient
# Inputs: Client_ID
# Outputs: Num Jobs, Job_ID, TODO: Active/Not Active
def getAllInfoAboutClient(db, Client_ID):
    doc_ref = db.collection("Clients").document(Client_ID).collection("Jobs")
    docs = doc_ref.get()
    document_ids = [doc.id for doc in docs]  # Use `doc.id` to get the document ID
    # print(len(docs))
    # print("Document IDs:", document_ids)
    
    return {"num_jobs": len(docs), "Job_IDs": document_ids}

## getAllInfoAboutJob
# Inputs: Client_ID, Job_ID
# Outputs: Start_Time, Model, TODO: Active/Not Active
def getAllInfoAboutJob(db, Client_ID,Job_ID):
    doc_ref = db.collection("Clients").document(Client_ID).collection("Jobs").document(Job_ID).collection("Job Data").document("Orchestrator Information")
    docs = doc_ref.get()
    data = docs.to_dict()
    
    Model = data["Model"]
    Start_Time = data["Start_Time"].astimezone(pytz.timezone('US/Eastern'))
    Start_Time_String = Start_Time.strftime("%A, %B %d, %Y at %I:%M:%S %p %Z")
    
    return {"Model": Model, "Start_Time": Start_Time_String}

    
## getJobStatistics
# Inputs: Client_ID, Job_ID
# Outputs: Start_Time, Model, average_time, average_time_after_llm, average_time_before_llm, average_time_in_llm
def getJobStatistics(db, Client_ID,Job_ID):
    doc_ref = db.collection("Clients").document(Client_ID).collection("Jobs").document(Job_ID).collection("Job Data").document("Stats")
    docs = doc_ref.get()
    data = docs.to_dict()
        
    return data

## getErrorInformation
# Inputs: Client_ID, Job_ID
# Outputs: List of Error Logs
def getErrorInformation(db, Client_ID, Job_ID):
    exErrorLogs = ["ROW 11 - OpenAI API returned a malformed response that could not be parsed.", 
                   "ROW 34 - An unexpected internal error occurred with the OpenAI API.",
                   "ROW 39 - OpenAI API failed to generate a valid response within the allocated time."]
            
    return exErrorLogs

## getErrorRows
# Inputs: Client_ID, Job_ID
# Outputs: List of Errors
def getErrorRows(db, Client_ID, Job_ID):
    doc_ref = db.collection("Clients").document(Client_ID).collection("Jobs").document(Job_ID).collection("Job Data").document("Errors")
    docs = doc_ref.get()
    data = docs.to_dict()
    error_rows = data["error_rows"]
        
    return error_rows


## produceInvoice
# Inputs: Client_ID, Job_ID
# Outputs: total_llm_cost, total_time, Start_Time, Client_ID, Job_ID, Model
def produceInvoice(db, Client_ID, Job_ID):
    doc_ref = db.collection("Clients").document(Client_ID).collection("Jobs").document(Job_ID).collection("Job Data").document("Orchestrator Information")
    docs = doc_ref.get()
    data = docs.to_dict()
    
    
    # Not sure if this works
    # total_time = data["Start_Time"] - data["End_Time"]
    total_time = 34
    
    Start_Time = data["Start_Time"].astimezone(pytz.timezone('US/Eastern'))
    Start_Time_String = Start_Time.strftime("%A, %B %d, %Y at %I:%M:%S %p %Z")
    
    invoiceData = {
        "total_llm_cost": .0032, # Hardcoded for now
        "Start_Time": Start_Time_String,
        "total_time": total_time, # Switch to total-time
        "Client_ID": data["Client_ID"],
        "Job_ID": data["Job_ID"],
        "Model": data["Model"]
    }
        
    return invoiceData





########################
# Performance Notebook #
########################

def runDashboard():
    # Example loop to update progress bar and clear output
    try:
        # Create placeholders for dynamic content
        display_handle = display("", display_id=True)
        
        while True:
            job_id = 1

            # Get the latest values from each endpoint (dummy example here)
            batch_processor_count = get_batch_processor_load(job_id)
            rate_limiter_count = get_rate_limiter_load(job_id)
            reverse_batch_processor_count = get_reverse_batch_processor_load(job_id)
            total_rows = get_total_rows(job_id)
            queue_1_count = get_queue_1_load(job_id)
            queue_2_count = get_queue_2_load(job_id)

            # Create the updated content
            output_html = f"""
            <h3>### Live Processor Counts ###</h3>
            <p>Batch Processor Count: {batch_processor_count} / {total_rows}</p>
            <p>Queue 1 Count: {queue_1_count} / {total_rows}</p>
            <p>Rate Limiter Count: {rate_limiter_count} / {total_rows}</p>
            <p>Queue 2 Count: {queue_2_count} / {total_rows}</p>
            <p>Reverse Batch Processor Count: {reverse_batch_processor_count} / {total_rows}</p>
            """

            # Update the display content without flashing
            display_handle.update(HTML(output_html))

            # Wait for half a second before updating
            time.sleep(0.2)

    except KeyboardInterrupt:
        print("Stopped updating.")

# Progress #
## getBatchProcessorLoad

## getQueue1Load

## getRateLimiterLoad

## getQueue2Load

## getReverseBatchProcessorLoad

## getTotalLoad

# Statistics #
## Start_Time

## End_Time

## Total_Time

## Average_Time


# getAllClients()
# print(getAllInfoAboutClient("rayan syed"))
# print(getAllInfoAboutJob("rayan syed","Job 466f47f2-6a5e-4ee1-9603-661095296532"))
# print(getJobStatistics("rayan syed","Job 466f47f2-6a5e-4ee1-9603-661095296532"))
# print(getErrorInformation("rayan syed","Job 466f47f2-6a5e-4ee1-9603-661095296532"))
# print(produceInvoice("rayan syed","Job 466f47f2-6a5e-4ee1-9603-661095296532"))





