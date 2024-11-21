from google.cloud import firestore

def logProgressWriter(Job_ID:str, Client_ID:str, Processed_Rows: int, Num_Rows:int):
    try:
        db = firestore.Client(project="elated-scope-437703-h9")
        doc_ref = db.collection("Clients").document(Client_ID).collection("Jobs").document("Job "+ Job_ID).collection("Job Data").document("Progress")
        doc_ref.set({
            "current_row": Processed_Rows,
            "total_rows": Num_Rows
        })
        print(f"Updated progress for {Client_ID}'s job {Job_ID}")

    except Exception as e:
        print(f"Unexpected error writing progress to firestore: {e}")