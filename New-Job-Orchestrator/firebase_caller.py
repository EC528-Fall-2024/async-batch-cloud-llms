

from firebase_helper_files import writeJobOrchestratorInformation, logProgressWriter
from google.cloud import firestore



Message_Data = {
	"User_Project_ID": "Example_Project_ID",
	"User_Dataset_ID": "Example_Dataset_ID",
	"Input_Table_ID": "Example_Dataset_ID",
	"Output_Table_ID": "Output_Table_ID",
	"Model": "gpt-3.5-turbo",
	"API_key": "api_key"
}

Attributes = {
	"Job_ID": "1",
	"Client_ID": "Client_1"
}

db = firestore.Client()

# Uncomment to write Num_Rows to firebase
Num_Row = 14
logProgressWriter(db, Attributes["Job_ID"], Attributes["Client_ID"], Num_Row)

# Uncomment to write meta data to firebase
# writeJobOrchestratorInformation(db, Attributes["Job_ID"], Attributes["Client_ID"], Message_Data["User_Project_ID"], Message_Data["User_Dataset_ID"], Message_Data["Input_Table_ID"], Message_Data["Output_Table_ID"], Message_Data["Model"], Message_Data["API_key"])



