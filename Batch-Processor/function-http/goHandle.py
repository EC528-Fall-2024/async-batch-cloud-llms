import time
from BigQueryReader import read_from_database, get_database_length
from pubSubSender import pubSubSender
from performance import decrementBatchProcessor, incrementQueue1, setBatchProcessor, setTotalCount, resetSystem
from pubSubSender import send_metrics

def goHandle(Job_ID:str, Client_ID:str, User_Project_ID:str, User_Dataset_ID:str, Input_Table_ID:str, Output_Table_ID:str, Model:str, API_key:str):
    
    # Get database length from input table dynamically
    Database_Length = get_database_length(User_Project_ID, User_Dataset_ID, Input_Table_ID)
    
    # Performance calls
    try:
        resetSystem(Job_ID)
        setBatchProcessor(Job_ID)
        setTotalCount(Job_ID)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    for i in range(1, int(Database_Length) + 1): 
        # record start time in stats collector
        send_metrics(Client_ID, Job_ID, i, time.time())
        
        # Read the database
        rowFromDatabase = read_from_database(i, Job_ID, Client_ID, User_Project_ID,  User_Dataset_ID, Input_Table_ID)
        
        if rowFromDatabase is not None: 
            pubSubSender(i, rowFromDatabase,Job_ID, Client_ID, User_Project_ID, User_Dataset_ID, Output_Table_ID, Model, API_key, Database_Length)
            print(f"Prompt and Text for row {i} read successfully.")
            
            # # Performance calls
            try:
                decrementBatchProcessor(Job_ID)
                incrementQueue1(Job_ID)
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

    # Return status
    return True
    
