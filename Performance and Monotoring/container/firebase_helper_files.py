from count_data_class import CountData
from google.cloud import firestore



############
# Firebase #
############
def clear_counts(db, Job_ID):
    # db = firestore.Client()
    # [START firestore_setup_dataset_pt1]
    doc_ref = db.collection("Jobs").document("Job "+ str(Job_ID)).collection("Job Data").document("Counts")
        # doc_ref.set({"first": "Ada", "last": "Lovelace", "born": 1815})
    doc_ref.set({
        "total_count": 0,
        "batch_processor_count": 0,
        "reverse_batch_processor_count": 0,
        "rate_limiter_count": 0,
        "queue_1_count": 0,
        "queue_2_count": 0
    })
    
    doc_ref = db.collection("Jobs").document("Job "+ str(Job_ID)).collection("Job Data").document("Time Stamps")
        # doc_ref.set({"first": "Ada", "last": "Lovelace", "born": 1815})
    doc_ref.set({
        "start_time": 0,
        "end_time": 0
    })
    
    
def setCount(db, Job_ID, Microservice, Count):
    doc_ref = db.collection("Jobs").document("Job "+ str(Job_ID)).collection("Job Data").document("Counts")
    doc_ref.update({ Microservice:  Count })
    
    if(Microservice == "batch_processor_count"):
        setTime(db, Job_ID, "start_time", firestore.SERVER_TIMESTAMP)

        

    
def setTime(db, Job_ID, TypeOfTime, CurrentTime):
    # db = firestore.Client()
    doc_ref = db.collection("Jobs").document("Job "+ str(Job_ID)).collection("Job Data").document("Time Stamps")
    doc_ref.update({ TypeOfTime:  CurrentTime })
    
    

def incrementFirestore(db, Job_ID, Microservice):
    doc_ref = db.collection("Jobs").document("Job " + str(Job_ID)).collection("Job Data").document("Counts")
    
    # Retrieve the current counts from Firestore
    counts = doc_ref.get().to_dict()
    
    # Extract the current count for the microservice and the total count
    current_count = counts.get(Microservice + "_count", 0)
    total_count = counts.get("total_count", 0)
    
    # Increment the count of the specified microservice
    doc_ref.update({
        (Microservice + "_count"): firestore.Increment(1)
    })
    
    # If the microservice is "rate limiter" and counts match, call `setTime`
    if Microservice == "reverse_batch_processor" and (current_count + 1) == total_count:
        # Call setTime to update the timestamp in the "Time Stamps" document
        setTime(db, Job_ID, "end_time", firestore.SERVER_TIMESTAMP)
    

def calculateStats(db, Job_ID):
    ## get start, end and total count
    doc_ref = db.collection("Jobs").document("Job "+ str(Job_ID)).collection("Job Data").document("Counts")
    counts = doc_ref.get().to_dict()
    
    # Extract the current count for the microservice and the total count
    total_count = counts.get("total_count", 0)
    
    doc_ref = db.collection("Jobs").document("Job "+ str(Job_ID)).collection("Job Data").document("Time Stamps")
    counts = doc_ref.get().to_dict()
    
    # Extract the current count for the microservice and the total count
    end_time = counts.get("end_time", 0)
    start_time = counts.get("start_time", 0)
    
    total_time = end_time - start_time
    
    total_time_seconds = total_time.total_seconds()
    average_time_seconds = total_time_seconds / total_count
    
    doc_ref = db.collection("Jobs").document("Job "+ str(Job_ID)).collection("Job Data").document("Stats")
    
    doc_ref.update({
        "average_time": average_time_seconds,
        "total_time": total_time_seconds,   
    })

def queryStats(db, Job_ID):
    doc_ref = db.collection("Jobs").document("Job "+ str(Job_ID)).collection("Job Data").document("Time Stamps")
    counts = doc_ref.get().to_dict()
    
    # Extract the current count for the microservice and the total count
    end_time = counts.get("end_time", 0)
    start_time = counts.get("start_time", 0)
    
    
    doc_ref = db.collection("Jobs").document("Job "+ str(Job_ID)).collection("Job Data").document("Stats")
    counts = doc_ref.get().to_dict()
    
    # Extract the current count for the microservice and the total count
    total_time = counts.get("total_time", 0)
    average_time = counts.get("average_time", 0)
    
    returnData = {
        "start_time": start_time,
        "end_time": end_time,
        "total_time": total_time,
        "average_time": average_time
    }
    
    return returnData
    
def decrementFirestore(db, Job_ID, Microservice):
    doc_ref = db.collection("Jobs").document("Job "+ str(Job_ID)).collection("Job Data").document("Counts")
        # doc_ref.set({"first": "Ada", "last": "Lovelace", "born": 1815})
        
    doc_ref.update({
        (Microservice + "_count"):  firestore.Increment(-1)
    })
    
    # Return status of the write
    return True

def getAllFirestore(db, Job_ID):
    # db = firestore.Client()

    doc_ref = db.collection("Jobs").document("Job "+ str(Job_ID)).collection("Job Data").document("Counts")

    doc = doc_ref.get()
    countData = CountData.from_dict(doc.to_dict())
    return countData
    
    
def getMicroserviceCount(db, Job_ID, Microservice):
    # db = firestore.Client()

    doc_ref = db.collection("Jobs").document("Job "+ str(Job_ID)).collection("Job Data").document("Counts")

    doc = doc_ref.get()
    countData = CountData.from_dict(doc.to_dict())
    
    return getattr(countData, (Microservice + "_count"))