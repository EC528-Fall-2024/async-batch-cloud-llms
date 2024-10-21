'''Tokenizer prototype'''
from openai import OpenAI
import tiktoken 

# OpenAI client
client = OpenAI(api_key="")

# Initialize the correct encoding for the OpenAI model
encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

def openai_tokenizer(messages) -> int:
    # Overpredict amnt of tokens needed
    total_tokens = 0

    for message in messages:
        total_tokens += len(encoding.encode(message["role"]))
        total_tokens += len(encoding.encode(message["content"]))
        total_tokens += 2  # <im_start> and <im_end>

    total_tokens += 2  # For message start/end separators

    # Add large buffer for safety
    buffer = int(0.2 * total_tokens)  
    total_tokens += buffer

    # Add estimated reply size (scaled for longer responses)
    total_tokens += 100  # arbitrary amnt to represent long response

    return total_tokens

def call_openai():
    # Make a call to the OpenAI API and track token usage
    try:
        # input
        messages = [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "What's 1+1?"},
                ]
        
        # Predict the number of tokens
        predicted_tokens = openai_tokenizer(messages)
        print(f"Predicted token usage: {predicted_tokens} tokens")

        # API Call
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        # Results
        print(f"Used {response.usage.total_tokens} tokens")
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"OpenAI API call failed: {e}")
        return None

print(call_openai())