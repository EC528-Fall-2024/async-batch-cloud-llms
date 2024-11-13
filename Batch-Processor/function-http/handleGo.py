from BigQueryReader import read_from_database
from ErrorLogger import error_message
from pubSubSender import pubSubSender

def handleGo(Job_ID, Client_ID, Database_Length):
    for i in range(1, int(Database_Length) + 1): 
        # Read the database
        rowFromDatabase = read_from_database(i, Job_ID, Client_ID)
        if rowFromDatabase is not None: 
            pubSubSender(i,rowFromDatabase,Job_ID, Client_ID)
            print(f"Prompt and Text for row {i} read successfully.")

    # Return status
    return True
    
