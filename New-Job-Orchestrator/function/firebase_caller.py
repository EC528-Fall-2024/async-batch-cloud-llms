

from firebase_helper_files import writeJobOrchestratorInformation


Attributes = {
	"Job_ID": "1",
	"Client_ID": "Rick Sorkin"
}

# Uncomment to write meta data to firebase

#db = firestore.Client()
#writeJobOrchestratorInformation(Attributes["Job_ID"], Attributes["Client_ID"], Message_Data["User_Project_ID"], Message_Data["User_Dataset_ID"], Message_Data["Input_Table_ID"], Message_Data["Output_Table_ID"], Message_Data["Model"], Message_Data["API_key"])



