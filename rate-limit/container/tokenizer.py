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

    # Add large buffer for safety
    buffer = int(0.2 * total_tokens)  
    total_tokens += buffer

    # Add estimated reply size (scaled for longer responses)
    total_tokens += 100  # arbitrary amnt to represent long response

    return total_tokens