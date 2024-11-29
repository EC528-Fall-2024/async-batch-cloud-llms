from flask import Flask, request, jsonify
from google.cloud import firestore
import os

from firebase_helper_files import clear_counts, setCount, incrementFirestore, decrementFirestore, getAllFirestore, getMicroserviceCount, calculateStats, queryStats

app = Flask(__name__)


@app.route('/test')
def hello():
    return 'Hello, World!'


# Types of microservice
# batch_processor
# reverse_batch_processor
# rate_limiter

# project_ID = "elated-scope-437703-h9"
db = firestore.Client()


###########
# Helpers #
###########
@app.route('/resetSystem')
def resetSystem():

    data = request.get_json()
    client_ID = data.get("Client_ID")
    job_ID = data.get("Job_ID")
    
    clear_counts(db, job_ID)

    print("Resetting the system")
    
    return jsonify({"response": 'All counts have been reset' }), 200

#############
# Analytics #
#############
@app.route('/setStats')
def setStats():

    data = request.get_json()
    client_ID = data.get("Client_ID")
    job_ID = data.get("Job_ID")
    
    calculateStats(db, client_ID, job_ID)

    print("Resetting the system")
    
    return jsonify({"stats": 'all stats have been calculated' }), 200

@app.route('/getStats')
def getStats():

    data = request.get_json()
    client_ID = data.get("Client_ID")
    job_ID = data.get("Job_ID")
    
    returnData = queryStats(db, client_ID, job_ID)
    print(returnData)
    
    return jsonify({"returnData": returnData }), 200


###########
# Setters #
###########
# Set Total (called from Batch Processor)
@app.route('/setTotalCount')
def setTotalCount():
    data = request.get_json()
    
    # Extract the `inputBatchCount` field, with error handling
    total_count = data.get("total_count")
    client_ID = data.get("Client_ID")
    job_ID = data.get("Job_ID")

    setCount(db, client_ID, job_ID, "total_count",total_count)
        
    return jsonify({"response": 'The total_count has been set' }), 200
    
# Set the "total" of the batch processor (Called from the batch processor)
@app.route('/setBatchProcessorCount')
def setBatchProcessorCount():
    data = request.get_json()
    
    client_ID = data.get("Client_ID")
    job_ID = data.get("Job_ID")
    total_count = data.get("batch_processor_count")

    
    setCount(db, client_ID, job_ID, "batch_processor_count",total_count)

    return jsonify({"response": 'The batch_processor_count set' }), 200 


################
# Decrementers #
################
@app.route('/decrementService')
def decrementService():
        
    data = request.get_json()
    client_ID = data.get("Client_ID")
    job_ID = data.get("Job_ID")
    microservice = data.get("Microservice")
    
    status = decrementFirestore(db, client_ID, job_ID, microservice)
    
    return jsonify({"Status": (microservice + ': ' +  str(status))}), 200



################
# Incrementers #
################
@app.route('/incrementService')
def incrementService():
    global rate_limiter_count
    
    data = request.get_json()
    client_ID = data.get("Client_ID")
    job_ID = data.get("Job_ID")
    microservice = data.get("Microservice")
    
    status = incrementFirestore(db, client_ID, job_ID, microservice)
    
    return jsonify({"Status": (microservice + ': ' +  str(status))}), 200



###########
# Getters #
###########
# Get Batch Processor Count
@app.route('/getCount')
def getBatchProcessorLoad():
    
    data = request.get_json()
    client_ID = data.get("Client_ID")
    job_ID = data.get("Job_ID")
    microservice = data.get("Microservice")
    
    countValue = getMicroserviceCount(db, client_ID, job_ID, microservice)

    return jsonify({(microservice + "_count"): countValue}), 200


## Currentlu broken
@app.route('/getAllInfo')
def getAllInfo():
    
    data = request.get_json()
    job_ID = data.get("Job_ID")
    
    
    allInfo = getAllFirestore(db, client_ID, job_ID)
    print(allInfo)
        
    return jsonify({"total_count": str(allInfo)}), 200
    # return jsonify({"total_count": "all Info"}), 200



# Error handling example
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404

if __name__ == "__main__":
    # testCalls()
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8089)))

    # app.run(port= 8084, debug=True)