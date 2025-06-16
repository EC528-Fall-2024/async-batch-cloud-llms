'''Tokenizer'''
import tiktoken
import math

# Tokenizer 
def openai_tokenizer(messages, model) -> int:
    # Initialize tokenizer
    tokenizer = tiktoken.encoding_for_model(model) 

    # Overpredict amnt of tokens needed
    total_tokens = 0
    for message in messages:
        total_tokens += len(tokenizer.encode(message["role"]))
        total_tokens += len(tokenizer.encode(message["content"]))
        total_tokens += 2  # <im_start> and <im_end>

    token_input = total_tokens

    total_tokens = int(math.ceil(1.0089 * token_input + 112))

    return token_input, total_tokens

def cost_estimator(model, token_input, actual_tokens):
    if model == "gpt-3.5-turbo":
        # Pricing for GPT-3.5-Turbo
        input_token_cost = 0.0015 / 1000  # $0.0015 per 1,000 input tokens
        output_token_cost = 0.02 / 1000   # $0.02 per 1,000 output tokens

        # Calculate costs
        token_output = max(actual_tokens - token_input, 0)
        input_cost = token_input * input_token_cost
        output_cost = token_output * output_token_cost
        total_cost = input_cost + output_cost
    
    return total_cost