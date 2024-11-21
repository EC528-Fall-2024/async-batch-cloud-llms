
from google.cloud import firestore


# write a function that given, job ID and client ID, will return the total_count and current_row
def getProgress(Job_ID, Client_ID):
    
    db = firestore.Client()

    doc_ref = db.collection("Clients").document(Client_ID).collection("Jobs").document("Job "+ Job_ID).collection("Job Data").document("Progress")
    doc = doc_ref.get()
    
    progress_data = doc.to_dict()
    
    return {
        "current_row": progress_data.get("current_row", 0),
        "total_rows": progress_data.get("total_rows", 0)
    }

