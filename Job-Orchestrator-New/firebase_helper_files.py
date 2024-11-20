from google.cloud import firestore


############
# Firebase #
############
def writeJobOrchestratorInformation(db, Job_ID:int, Client_ID:str, User_Project_ID:str, User_Dataset_ID:str, Input_Table_ID:str, Output_Table_ID:str, Model:str, API_key:str):
    # db = firestore.Client()
    # [START firestore_setup_dataset_pt1]
    doc_ref = db.collection("Jobs").document("Job "+ str(Job_ID)).collection("Job Data").document("Orchestrator Information")
        # doc_ref.set({"first": "Ada", "last": "Lovelace", "born": 1815})
    doc_ref.set({
        "User_Project_ID": "Example_Project_ID",
        "User_Dataset_ID": "Example_Dataset_ID",
        "Input_Table_ID": "Example_Dataset_ID",
        "Output_Table_ID": "Output_Table_ID",
        "Model": "gpt-3.5-turbo",
        "API_key": "api_key",
        "Job_ID": "Job_ID",
	    "Client_ID": "Client_1"
    })
    

    