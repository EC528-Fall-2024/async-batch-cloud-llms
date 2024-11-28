'''Rate Limiter'''
import time
from tokenizer import openai_tokenizer
from RequestLimiter import incr_request
from UserBucket import update_user_bucket, get_tokens_from_user, shrink_user_bucket
from CallOpenAI import call_openai, valid_model, format_messages
from Publisher import send_response, send_metrics
from logger import error_message

token_limit = 200000 # token/min

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
        api_key = None # to trigger sample response

    if not valid_model(model):
        errormessage = f"Invalid model {model}. Aborting row {row}"
        print(errormessage)
        error_message(errormessage, job_id, user_id, "RowDropped", row)
        return

    # Format message for OpenAI
    messages = format_messages(message)
    
    # Predict needed tokens
    tokens_needed = openai_tokenizer(messages, model)
    print(f"Predicting {tokens_needed} tokens needed")

    # Try to initialize/update that user's subbucket
    if not update_user_bucket(user_id, tokens_needed):
        errormessage = f"Failed to update user bucket. Aborting row {row}"
        print(errormessage)
        error_message(errormessage, job_id, user_id, "RowDropped", row)
        return

    # Try to call LLM API
    if get_tokens_from_user(user_id, tokens_needed):
        print("Attempting to call OpenAI...") 

        # Get request approved by request limiter before retry
        if not incr_request():
            errormessage = f"Error with request limiter. Aborting row {row}"
            print(errormessage)
            error_message(errormessage, job_id, user_id, "RowDropped", row)
            return
        
        # Call LLM API & record metrics
        in_llm = time.time()
        response_content, actual_tokens, counter = call_openai(messages, user_id, tokens_needed, token_limit, api_key, model)
        out_llm = time.time()

        # Send metrics to status collector
        send_metrics(user_id, job_id, row, in_llm, out_llm)

        if response_content is None:
            errormessage = f"OpenAI API call failed, sending back tokens & aborting row {row}"
            print(errormessage)
            error_message(errormessage, job_id, user_id, "RowDropped", row)
            shrink_user_bucket(user_id,min(tokens_needed*counter,token_limit), actual_tokens)
            return
        print(f"Received Response: {response_content}")

        # Response Logic
        send_response(user_id, job_id, job_length, row, response_content, user_project_id, user_dataset_id, output_table_id)

        # Shrink user bucket accordingly since job complete
        shrink_user_bucket(user_id,min(tokens_needed*counter,token_limit), actual_tokens)
    else:
        errormessage = f"Issue with accessing tokens from user bucket. Aborting row {row}"
        print(errormessage)
        error_message(errormessage, job_id, user_id, "RowDropped", row)