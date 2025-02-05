import time
from BigQueryReader import read_from_database, get_database_length
from pubSubSender import pubSubSender, send_metrics
from performance import decrementBatchProcessor, incrementQueue1, setBatchProcessor, setTotalCount, resetSystem

def goHandle(Job_ID:str, Client_ID:str, User_Project_ID:str, User_Dataset_ID:str, Input_Table_ID:str, Output_Table_ID:str, Model:str, API_key:str):
    
    # Get database length from input table dynamically
    Database_Length = get_database_length(User_Project_ID, User_Dataset_ID, Input_Table_ID)
    
    # Performance API calls
    # try:
    #     resetSystem(Job_ID)
    #     setBatchProcessor(Job_ID)
    #     setTotalCount(Job_ID)
    # except Exception as e:
    #     print(f"An unexpected error occurred: {e}")

    # batch size for reading from BigQuery
    batch_size = 100

    for i in range(1, int(Database_Length) + 1, batch_size): 

        # record start time in stats collector for each row
        for row in range(i, min(i + batch_size, int(Database_Length) + 1)):
            send_metrics(Client_ID, Job_ID, row, time.time())
        
        # Read the database
        rows = read_from_database(i, batch_size, Job_ID, Client_ID, User_Project_ID,  User_Dataset_ID, Input_Table_ID)
        
        for idx, rowFromDatabase in enumerate(rows, start=i):
            if rowFromDatabase is not None: 
                pubSubSender(idx, rowFromDatabase, Job_ID, Client_ID, User_Project_ID, User_Dataset_ID, Output_Table_ID, Model, API_key, Database_Length)
                print(f"Prompt and Text for row {idx} read successfully.")
                
                # Performance calls
                # try:
                #     decrementBatchProcessor(Job_ID)
                #     incrementQueue1(Job_ID)
                # except Exception as e:
                #     print(f"An unexpected error occurred for updating performance API metrics: {e}")

    # Return status
    return True
    
