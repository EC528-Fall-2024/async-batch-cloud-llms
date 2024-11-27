from google.cloud import firestore

# increment rows completed in firestore
def logProgressWriter(Job_ID:str, Client_ID:str, Processed_Rows: int, Num_Rows:int):
    try:
        db = firestore.Client()
        doc_ref = db.collection("Clients").document(Client_ID).collection("Jobs").document("Job "+ Job_ID).collection("Job Data").document("Progress")
        doc_ref.set({
            "current_row": Processed_Rows,
            "total_rows": Num_Rows
        })
        print(f"Updated progress for {Client_ID}'s job {Job_ID}")

    except Exception as e:
        print(f"Unexpected error writing progress to firestore: {e}")

# convey what rows have been dropped for a job in firestore 
def rowErrorWriter(Job_ID, Client_ID, Failed_Row):
    try:
        db = firestore.Client()
        doc_ref = db.collection("Clients").document(Client_ID).collection("Jobs").document("Job "+ Job_ID).collection("Job Data").document("Progress")
        # Use a transaction to ensure atomic updates 
        with db.transaction(): 
            doc = doc_ref.get() 
            if doc.exists: 
                doc_ref.update({ 'error_rows': firestore.ArrayUnion([Failed_Row]) }) # Append failed row
            else: 
                doc_ref.set({ 'error_rows': [Failed_Row] }) # New list of failed rows starting with this row
        print(f"Updated error row to fire store for job {Job_ID}")

    except Exception as e:
        print(f"Unexpected error appending error row to firestore: {e}")