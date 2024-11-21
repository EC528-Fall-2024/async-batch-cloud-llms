from google.cloud import firestore


def writeJobOrchestratorInformation(Job_ID:int, Client_ID:str, User_Project_ID:str, User_Dataset_ID:str, Input_Table_ID:str, Output_Table_ID:str, Model:str, API_key:str):
    
    try:
        db = firestore.Client()
        doc_ref = db.collection("Clients").document(Client_ID).collection("Jobs").document("Job "+ str(Job_ID)).collection("Job Data").document("Orchestrator Information")
        doc_ref.set({
            "User_Project_ID": User_Project_ID,
            "User_Dataset_ID": User_Dataset_ID,
            "Input_Table_ID": Input_Table_ID,
            "Output_Table_ID": Output_Table_ID,
            "Model": Model,
            "API_key": API_key,
            "Job_ID": str(Job_ID),
            "Client_ID": Client_ID
        })
        
        print(f"Wrote job {Job_ID} metadata to firestore successfully.")

    except Exception as e:
        print(f"Unexpected error writing log to firestore: {e}")