from firebase_helper_files import getProgress

Job_ID = "1"
Client_ID = "Rick Sorkin"

progressData = getProgress(Job_ID, Client_ID)

print("current_row: " + str(progressData["current_row"]))
print("total_row: " + str(progressData["total_rows"]))