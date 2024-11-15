'''Rate Limiter'''
from tokenizer import openai_tokenizer
from RequestLimiter import incr_request
from UserBucket import update_user_bucket, get_tokens_from_user, shrink_user_bucket
from CallOpenAI import call_openai, valid_model, format_messages
from Publisher import send_response

token_limit = 200000 # token/min
refill_time = 60 # min

# Send batch through rate-limiter
def rate_limit(batch):
    user_id = batch['client_id'] 
    message = batch['message']
    job_id = batch['job_id']
    job_length = int(batch['job_length'])
    user_project_id = batch['user_project_id']
    row = batch['row']
    model = batch['model']
    user_dataset_id = batch['user_dataset_id']
    output_table_id = batch['output_table_id']
    model = batch['model']
    api_key = batch['api_key']
    if api_key == "":
        api_key = None

    if not valid_model(model):
        print(f"Invalid model {model}, dropping row for {job_id}")
        return

    # Format message for OpenAI
    messages = format_messages(message)
    
    # Predict needed tokens
    tokens_needed = openai_tokenizer(messages, model)
    print(f"Predicting {tokens_needed} tokens needed")

    # Try to initialize/update that user's subbucket
    if not update_user_bucket(user_id, tokens_needed):
        print("Failed to initialize sub-bucket. Aborting batch.")
        return

    # Try to call LLM API
    if get_tokens_from_user(user_id, tokens_needed, refill_time):
        print("Attempting to call OpenAI...") 

        # Get request approved by request limiter before retry
        if not incr_request():
            print("Error with request limiter, aborting batch")
            return
        
        # Call LLM API
        response_content, actual_tokens, counter = call_openai(messages, user_id, tokens_needed, token_limit, api_key, model)
        if response_content is None:
            print("OpenAI API call failed, sending back tokens & aborting")
            shrink_user_bucket(user_id,min(tokens_needed*counter,token_limit), actual_tokens, refill_time)
            return
        print(f"Received Response: {response_content}")

        # Response Logic
        send_response(user_id, job_id, job_length, row, response_content, user_project_id, user_dataset_id, output_table_id)

        # Shrink user bucket accordingly since job complete
        shrink_user_bucket(user_id,min(tokens_needed*counter,token_limit), actual_tokens,refill_time)
    else:
        print("Issue with accessing tokens from user bucket. Aborting batch")