import ollama
import os
import datetime

MODEL = 'gemma3:1b'  # default small model
TRANSCRIPTS_DIR = '../transcripts/'

def query_ollama(messages, model: str) -> str:
    """Call Ollama with the user prompt and return the reply text."""
    # Use ollama.chat(...) with role="user" and return the text response.
    try:
        response = ollama.chat(model=model, messages=messages)
        return response.message.content or ''
    except ollama.ResponseError as e:
        return f'Error: {e.error}'
    

def main():
    today = datetime.date.today()
    TRANSCRIPT_PATH = os.path.join(TRANSCRIPTS_DIR, str(today))
    os.makedirs(TRANSCRIPT_PATH, exist_ok=True)

    file_name = f'{datetime.datetime.now().replace(microsecond=0).isoformat()}.txt'
    file_path = os.path.join(TRANSCRIPT_PATH, file_name)
    

    print('/exit to quit')
    messages = []

    while True:
        user_input = input(">>>").strip()

        if user_input == '/exit': break
        if user_input == '/new': 
            messages = []
            print("In-memory history cleared.")
            continue

        messages.append({'role': 'user', 'content': user_input})
        with open(file_path, 'a') as f:
            f.write(f"[{datetime.datetime.now().replace(microsecond=0).isoformat()}] [user]: {user_input}\n")

        response = query_ollama(messages, MODEL)

        messages.append({'role': 'assistant', 'content': response})
        with open(file_path, 'a') as f:
            f.write(f"[{datetime.datetime.now().replace(microsecond=0).isoformat()}] [{MODEL}]: {response}\n")

        print(response)


if __name__ == "__main__":
    main()