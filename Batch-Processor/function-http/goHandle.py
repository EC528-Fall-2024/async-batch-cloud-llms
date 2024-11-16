from BigQueryReader import read_from_database
from ErrorLogger import error_message
from pubSubSender import pubSubSender


def goHandle(Job_ID:str, Client_ID:str, User_Project_ID:str, User_Dataset_ID:str, Input_Table_ID:str, Output_Table_ID:str, Model:str, API_key:str):
    
    # Currently hardcoded, will be quried soon
    Database_Length = 13
    
    for i in range(1, int(Database_Length) + 1): 
        # Read the database
        rowFromDatabase = read_from_database(i, Job_ID, Client_ID, User_Project_ID,  User_Dataset_ID, Input_Table_ID)
        
        if rowFromDatabase is not None: 
            pubSubSender(i,rowFromDatabase,Job_ID, Client_ID, User_Project_ID, User_Dataset_ID, Output_Table_ID, Model, API_key, Database_Length)
            print(f"Prompt and Text for row {i} read successfully.")
 

    # Return status
    return True
    
