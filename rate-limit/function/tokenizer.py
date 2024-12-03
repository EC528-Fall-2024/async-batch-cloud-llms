'''Tokenizer'''
import tiktoken

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

    total_tokens += 2  # For message start/end separators

    token_input = total_tokens # done with estimate input message token length

    # Add large buffer for safety
    buffer = int(0.2 * total_tokens)  
    total_tokens += buffer

    # Add estimated reply size (scaled for longer responses)
    total_tokens += 100  # arbitrary amnt to represent long response

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