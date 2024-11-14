'''Rate Limiter'''
from tokenizer import openai_tokenizer
from RequestLimiter import incr_request
from UserBucket import update_user_bucket, get_tokens_from_user, shrink_user_bucket
from CallOpenAI import call_openai
from Publisher import send_response

token_limit = 200000 # token/min
refill_time = 60 # min

# Send batch through rate-limiter
def rate_limit(batch):
    user_id = batch['client_id'] 
    message = batch['message']
    job_id = batch['job_id']
    row = batch['row']
    model = "gpt-3.5-turbo"
    api_key = None

    # Format message for OpenAI
    messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message},
            ]
    
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
        print(f"Received Response: {response_content}") # LOGGING

        # Response Logic
        send_response(user_id, job_id, row, response_content)

        # Shrink user bucket accordingly since job complete
        shrink_user_bucket(user_id,min(tokens_needed*counter,token_limit), actual_tokens,refill_time)
    else:
        print("Issue with accessing tokens from user bucket. Aborting batch")