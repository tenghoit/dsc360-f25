#!/usr/bin/env python3
# Part 1 of the minilab:
# Ask the model for the capital of a country, returning only the city name.
#
# See the Ollama Python API docs and examples here:
#   https://github.com/ollama/ollama-python
#
# You need to:
#   - complete query_ollama() so it calls the API
#   - complete main() to build the prompt and print the answer

import ollama

MODEL = "gemma3:1b"  # default small model

def query_ollama(prompt: str, model: str) -> str:
    """Call Ollama with the user prompt and return the reply text."""
    # Use ollama.chat(...) with role="user" and return the text response.
    try:
        stream =  ollama.chat(model=model, messages=[
            {
                'role':'user',
                'content': prompt,
            },
        ], stream=True)
        
        for chunk in stream:
            print(chunk.message.content, end='', flush=True)

        return stream.message.content or ''
    except ollama.ResponseError as e:
        return f'Error: {e.error}'


def main() -> None:
    """Ask for a country, build the prompt, call query_ollama, and print the answer."""
    # Example steps:
    # 1. Ask user for a country with input()
    # 2. Clean it up (strip spaces, title-case it)
    # 3. Build a prompt like "What is the capital of ___?"
    # 4. Call query_ollama() and print the answer
    country = input("Enter a country: ")
    prompt = f'What is the capital of {country}?'
    result = query_ollama(prompt=prompt, model=MODEL)
    print(result)
    

if __name__ == "__main__":
    main()
