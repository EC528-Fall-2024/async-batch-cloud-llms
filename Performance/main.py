from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/test')
def hello():
    return 'Hello, World!'

# Setters
# Decrementers
# Incrementers
# Getters

# Data
total_count = 0
batch_processor_count = 0
reverse_batch_processor_count = 0
rate_limiter_count = 0


###########
# Setters #
###########
# Set Total (called from Batch Processor)
@app.route('/setTotalCount')
def setTotal():
    global total_count  # Declare as global to modify the outer variable

    data = request.get_json()
    
    # Extract the `inputBatchCount` field, with error handling
    total_count = data.get("total_count")
    
    print("Setting the Total Rows of the Job")
    
    return jsonify({"response": 'The total_count has been set' }), 200
    
# Set the "total" of the batch processor (Called from the batch processor)
@app.route('/setBatchProcessorCount')
def setBatchProcessorCount():
    global batch_processor_count  # Declare as global to modify the outer variable

    data = request.get_json()
    
    # Extract the `inputBatchCount` field, with error handling
    batch_processor_count = data.get("batch_processor_count")
    
    print("Setting the load of the batch processor")
    
    return jsonify({"response": 'The batch_processor_count set' }), 200


################
# Decrementers #
################
# Decrement Batch Processor (called from Batch Processor)
@app.route('/decrementBatchProcessor')
def decrementBatchProcessor():
    global batch_processor_count
    
    batch_processor_count = batch_processor_count - 1
    print("Decrementing the Batch Processor")
    
    return jsonify({"response": 'Batch Processor Decremented' }), 200

# Decrement Rate Limiter (called from Rate Limiter)
@app.route('/decrementRateLimiter')
def decrementRateLimiter():
    global rate_limiter_count
    
    rate_limiter_count = rate_limiter_count - 1
    print("Decrementing the Rate Limiter")
    
    return jsonify({"response": 'Rate Limiter Decremented' }), 200

# Decrement Reverse Batch Processor (called from Rate Limiter)
@app.route('/decrementReverseBatchProcessor')
def decrementReverseBatchProcessor():
    global reverse_batch_processor_count
    
    reverse_batch_processor_count = reverse_batch_processor_count - 1
    print("Decrementing the Reverse Batch Processor")
    
    return jsonify({"response": 'Reverse Batch Processor Decremented'}), 200


################
# Incrementers #
################
# Increment Rate Limiter (called from batch processor)
@app.route('/incrementRateLimiter')
def incrementRateLimiter():
    global rate_limiter_count
    
    rate_limiter_count = rate_limiter_count + 1
    print("Incrementing the Rate Limiter")
    
    return jsonify({"response": 'Rate Limiter Incremented'}), 200

# Increment Reverse Batch Processor (called from Rate Limiter)
@app.route('/incrementReverseBatchProcessor')
def incrementReverseBatchProcessor():
    global reverse_batch_processor_count 
    
    reverse_batch_processor_count = reverse_batch_processor_count + 1
    print("Incrementing the Reverse Batch Processor")
    
    return jsonify({"response": 'Reverse Batch Processor Incremented'}), 200


###########
# Getters #
###########
# Get Batch Processor Count
@app.route('/getBatchProcessorLoad')
def getBatchProcessorLoad():

    print("Getting the Batch Processor Load")
    return jsonify({"batch_processor_count": batch_processor_count}), 200

# Get Rate Limiter Count
@app.route('/getRateLimiterLoad')
def getRateLimiterLoad():
    
    print("Getting the Rate Limiter Load")
    return jsonify({"rate_limiter_count": rate_limiter_count}), 200

# Get Reverse Batch Processor Count
@app.route('/getReverseBatchProcessorLoad')
def getReverseBatchProcessorLoad():
    
    print("Getting the Reverse Batch Processor Load")
    return jsonify({"reverse_batch_processor_count": reverse_batch_processor_count}), 200

# Get Total
@app.route('/getTotalRows')
def getTotalRows():
    
    print("Getting the total rows")
    return jsonify({"total_count": total_count}), 200


# Error handling example
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404

if __name__ == "__main__":
    app.run(port= 8084, debug=True)