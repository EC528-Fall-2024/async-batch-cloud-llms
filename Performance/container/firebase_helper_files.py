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
    # db = firestore.Client()
    doc_ref = db.collection("Jobs").document("Job "+ str(Job_ID)).collection("Job Data").document("Counts")
    doc_ref.update({ Microservice:  Count })
    
    
    
def incrementFirestore(db, Job_ID, Microservice):
    # db = firestore.Client()
    
    # [START firestore_setup_dataset_pt1]
    doc_ref = db.collection("Jobs").document("Job "+ str(Job_ID)).collection("Job Data").document("Counts")
        # doc_ref.set({"first": "Ada", "last": "Lovelace", "born": 1815})
    doc_ref.update({
        (Microservice + "_count"):  firestore.Increment(1)
    })
    
    # Return status of the write
    return True
    
    
def decrementFirestore(db, Job_ID, Microservice):
    # db = firestore.Client()
    
    # [START firestore_setup_dataset_pt1]
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