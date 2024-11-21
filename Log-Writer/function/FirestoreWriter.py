from google.cloud import firestore


def logProgressWriter(Job_ID:int, Client_ID:str, Num_Rows:int):
    db = firestore.Client()
    # [START firestore_setup_dataset_pt1]
    doc_ref = db.collection("Clients").document(Client_ID).collection("Jobs").document("Job "+ str(Job_ID)).collection("Job Data").document("Progress")
    doc_ref.set({
        "current_row": Num_Rows
    })