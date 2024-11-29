from google.cloud import firestore


def writeJobOrchestratorInformation(Job_ID:str, Client_ID:str, User_Project_ID:str, User_Dataset_ID:str, Input_Table_ID:str, Output_Table_ID:str, Model:str):
    
    try:
        db = firestore.Client()
        doc_ref = db.collection("Clients").document(Client_ID).collection("Jobs").document("Job "+ str(Job_ID)).collection("Job Data").document("Orchestrator Information")
        doc_ref.set({
            "User_Project_ID": User_Project_ID,
            "User_Dataset_ID": User_Dataset_ID,
            "Input_Table_ID": Input_Table_ID,
            "Output_Table_ID": Output_Table_ID,
            "Model": Model,
            "Job_ID": str(Job_ID),
            "Client_ID": Client_ID
        })
        
        print(f"Wrote job {Job_ID} metadata to firestore successfully.")

    except Exception as e:
        print(f"Unexpected error writing meteadata to firestore: {e}")
 
 
"""
Initialize the Firestore hierarchy for a given Client and Job.
Ensures existence of all collections and documents up to 'Job Data'.
"""       
def initializeJobHierarchy(Client_ID: str, Job_ID: str):
    try:
        db = firestore.Client()

        # Ensure "Clients" collection and Client document exist
        client_doc_ref = db.collection("Clients").document(Client_ID)
        if not client_doc_ref.get().exists:
            client_doc_ref.set({})  # Create an empty document
            print(f"Initialized Client document for Client_ID: {Client_ID}")

        # Ensure "Jobs" collection and Job document exist
        job_doc_ref = client_doc_ref.collection("Jobs").document("Job " + str(Job_ID))
        if not job_doc_ref.get().exists:
            job_doc_ref.set({})  # Create an empty document
            print(f"Initialized Job document for Job_ID: {Job_ID}")

        # Ensure "Job Data" sub-collection exists
        job_data_doc_ref = job_doc_ref.collection("Job Data").document("Orchestrator Information")
        if not job_data_doc_ref.get().exists:
            job_data_doc_ref.set({})  # Create a minimal document to initialize
            print(f"Initialized Job Data sub-collection for Job_ID: {Job_ID}")
            
                # Ensure "Job Data" sub-collection exists
        job_data_doc_ref = job_doc_ref.collection("Job Data").document("PerformanceAPI")
        if not job_data_doc_ref.get().exists:
            job_data_doc_ref.set({})  # Create a minimal document to initialize
            
                # Ensure "Job Data" sub-collection exists
        job_data_doc_ref = job_doc_ref.collection("Job Data").document("Progress")
        if not job_data_doc_ref.get().exists:
            job_data_doc_ref.set({})  # Create a minimal document to initialize
            
        job_data_doc_ref = job_doc_ref.collection("Job Data").document("Stats")
        if not job_data_doc_ref.get().exists:
            job_data_doc_ref.set({})  # Create a minimal document to initialize
            

        print(f"Hierarchy initialized successfully for Client_ID: {Client_ID}, Job_ID: {Job_ID}")

    except Exception as e:
        print(f"Error initializing hierarchy: {e}")
        
initializeJobHierarchy("rick sorkin", "job 2123")