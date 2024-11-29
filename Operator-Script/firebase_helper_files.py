from google.cloud import firestore
import pytz




#####################
# Operator Notebook #
#####################

## getAllClients
# Inputs: Null
# Outputs: Array of all Clients
def getAllClients():
    db = firestore.Client()
    doc_ref = db.collection("Clients")
    docs = doc_ref.get()
    document_ids = [doc.id for doc in docs]  # Use `doc.id` to get the document ID
    print("Document IDs:", document_ids)
    return document_ids


## getAllInfoAboutClient
# Inputs: Client_ID
# Outputs: Num Jobs, Job_ID, TODO: Active/Not Active
def getAllInfoAboutClient(Client_ID):
    db = firestore.Client()
    doc_ref = db.collection("Clients").document(Client_ID).collection("Jobs")
    docs = doc_ref.get()
    document_ids = [doc.id for doc in docs]  # Use `doc.id` to get the document ID
    # print(len(docs))
    # print("Document IDs:", document_ids)
    
    return {"num_jobs": len(docs), "Job_IDs": document_ids}

## getAllInfoAboutJob
# Inputs: Client_ID, Job_ID
# Outputs: Start_Time, Model, TODO: Active/Not Active
def getAllInfoAboutJob(Client_ID,Job_ID):
    db = firestore.Client()
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
def getJobStatistics(Client_ID,Job_ID):
    db = firestore.Client()
    doc_ref = db.collection("Clients").document(Client_ID).collection("Jobs").document(Job_ID).collection("Job Data").document("Stats")
    docs = doc_ref.get()
    data = docs.to_dict()
        
    return data

## getErrorInformation
# Inputs: Client_ID, Job_ID
# Outputs: List of Error Logs
def getErrorInformation(Client_ID, Job_ID):
    exErrorLogs = ["ROW 11 - OpenAI API returned a malformed response that could not be parsed.", 
                   "ROW 34 - An unexpected internal error occurred with the OpenAI API.",
                   "ROW 39 - OpenAI API failed to generate a valid response within the allocated time."]
            
    return exErrorLogs

## getErrorRows
# Inputs: Client_ID, Job_ID
# Outputs: List of Errors
def getErrorRows(Client_ID, Job_ID):
    db = firestore.Client()
    doc_ref = db.collection("Clients").document(Client_ID).collection("Jobs").document(Job_ID).collection("Job Data").document("Progress")
    docs = doc_ref.get()
    data = docs.to_dict()
    error_rows = data["error_rows"]
        
    return error_rows


## produceInvoice
# Inputs: Client_ID, Job_ID
# Outputs: total_llm_cost, total_time, Start_Time, Client_ID, Job_ID, Model
def produceInvoice(Client_ID, Job_ID):
    db = firestore.Client()
    doc_ref = db.collection("Clients").document(Client_ID).collection("Jobs").document(Job_ID).collection("Job Data").document("Orchestrator Information")
    docs = doc_ref.get()
    data = docs.to_dict()
    
    
    # Not sure if this works
    # total_time = data["Start_Time"] - data["End_Time"]
    total_time = 34
    
    invoiceData = {
        "total_llm_cost": .0032, # Hardcoded for now
        "Start_Time": data["Start_Time"],
        "total_time": total_time, # Switch to total-time
        "Client_ID": data["Client_ID"],
        "Job_ID": data["Job_ID"],
        "Model": data["Model"]
    }
        
    return invoiceData





########################
# Performance Notebook #
########################

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





