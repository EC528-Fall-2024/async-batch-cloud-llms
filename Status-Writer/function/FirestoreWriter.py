from google.cloud import firestore
import redis

redis_client = redis.Redis(host='10.84.53.171', port=6379, db=0)

# increment rows completed in firestore
def logProgressWriter(Job_ID:str, Client_ID:str, Processed_Rows: int, Num_Rows:int):
    try:
        # Use redis lock for updating firestore
        with redis_client.lock(f"{Client_ID}_{Job_ID}_progress_lock"):
            db = firestore.Client()
            doc_ref = db.collection("Clients").document(Client_ID).collection("Jobs").document("Job "+ Job_ID).collection("Job Data").document("Progress")
            doc = doc_ref.get()
            if not doc.exists:
                doc_ref.set({
                    "current_row": Processed_Rows,
                    "total_rows": Num_Rows
                })
            else:
                data = doc.to_dict()
                current_row = data.get("current_row", 0)
                Processed_Rows = max(Processed_Rows, current_row)
                doc_ref.update({
                    "current_row": Processed_Rows
                })
            print(f"Updated progress for {Client_ID}'s job {Job_ID}")

    except Exception as e:
        print(f"Unexpected error writing progress to firestore: {e}")

# convey what rows have been dropped for a job in firestore 
def rowErrorWriter(Job_ID, Client_ID, Failed_Row, Error_Message):
    try:
        # Use redis lock for updating firestore
        with redis_client.lock(f"{Client_ID}_{Job_ID}_error_lock"):
            db = firestore.Client()

            # First update error row lists
            doc_ref = db.collection("Clients").document(Client_ID).collection("Jobs").document("Job "+ Job_ID).collection("Job Data").document("Errors")
            # Use a transaction to ensure atomic updates 
            with db.transaction(): 
                doc = doc_ref.get() 
                if doc.exists: 
                    doc_ref.update({ 'error_rows': firestore.ArrayUnion([Failed_Row]) }) # Append failed row
                else: 
                    doc_ref.set({ 'error_rows': [Failed_Row] }) # New list of failed rows starting with this row
            print(f"Updated error row to fire store for job {Job_ID}")

            # Then update error string list
            # Use a transaction to ensure atomic updates 
            with db.transaction(): 
                doc = doc_ref.get() 
                if doc.exists: 
                    doc_ref.update({ 'error_row_messages': firestore.ArrayUnion([Error_Message]) }) # Append failed row message
                else: 
                    doc_ref.set({ 'error_row_messages': [Error_Message] }) # New list of failed row messages starting with this row
            print(f"Updated error row to fire store for job {Job_ID}")

    except Exception as e:
        print(f"Unexpected error appending error row to firestore: {e}")