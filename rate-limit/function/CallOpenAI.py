'''OpenAI Call'''
import openai
import time
from UserBucket import update_user_bucket
from RequestLimiter import incr_request

# Ensure model is supported by this solution
def valid_model(model):
    if model == "gpt-3.5-turbo":
        return True
    else:
        return False
    
# Format messages for OpenAI
def format_messages(message):
    messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message},
            ]
    return messages

# Attempt to call OpenAI API
def call_openai(messages, user_id, tokens_needed, token_limit, api_key, model, counter = 1, delay = 5):
    if api_key is not None:
        try:
            client = openai.OpenAI(api_key=api_key) 
        except:
            print("Failure to set-up OpenAI Client")
            return None, tokens_needed, counter
    else:
        # Send fake response for testing purposes
        time.sleep(1)
        return "sample response", tokens_needed, 1
    
    # Assume this job needs to be dropped if delay over 2 minutes
    if(delay>120):
        print("Unexpected error in call_openai")
        return None, tokens_needed, counter
    
    # Make a call to the OpenAI API and track actual token usage
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages
        )
        actual = response.usage.total_tokens
        return response.choices[0].message.content.strip(), actual, counter
    
    # If OpenAI API call fails, assume incorrect prediction of tokens
    except openai.RateLimitError as e: 
        print(f"OpenAI API rate limit has been reached, increasing {user_id}'s token bucket before retrying...")
        
        # If rate limit error, add tokens to the user bucket, caps at token_limit
        tokens_needed = min(token_limit-tokens_needed, tokens_needed)
        if not update_user_bucket(user_id, tokens_needed):
            print("Failed to update sub-bucket. Aborting batch.")
            return None, token_limit, counter
        if delay > 5: # no delay initially
            print(f"Trying to run request again for {user_id} after {delay} seconds") 
            time.sleep(delay)
            # Get request approved by request limiter before retry
            if not incr_request():
                print("Error with request limiter, aborting batch")
                return None, token_limit, counter

        # Exponential Backoff
        return call_openai(messages, user_id, tokens_needed, token_limit, api_key, model, counter+1, delay*2)

    # uncontrollable errors - LOGGING HERE
    except Exception as e:
        if isinstance(e, openai.APIConnectionError):
            error_message = f"OpenAI API Connection error: {e}"
        elif isinstance(e, openai.APITimeoutError):
            error_message = f"OpenAI API Timeout error:{e}"
        elif isinstance(e, openai.AuthenticationError):
            error_message = f"OpenAI Authentication error:{e}"
        elif isinstance(e, openai.BadRequestError):
            error_message = f"OpenAI Bad Request error:{e}"
        elif isinstance(e, openai.ConflictError):
            error_message = f"OpenAI Conflict error:{e}"
        elif isinstance(e, openai.InternalServerError):
            error_message = f"OpenAI Internal Server error:{e}"
        elif isinstance(e, openai.NotFoundError):
            error_message = f"OpenAI Not Found error:{e}"
        elif isinstance(e, openai.PermissionDeniedError):
            error_message = f"OpenAI Permission Denied error:{e}"
        elif isinstance(e, openai.UnprocessableEntityError):
            error_message = f"OpenAI Unprocessed Entity error: {e}"
        else:
            error_message = f"Unexpected error in call_openai: {e}"
        print(error_message) 
        return None, tokens_needed, counter