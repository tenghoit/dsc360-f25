import ollama
import os
import datetime


def query_ollama(messages, model: str) -> str:
    """Call Ollama with the user prompt and return the reply text."""
    # Use ollama.chat(...) with role="user" and return the text response.
    try:
        response = ollama.chat(model=model, messages=messages)
        return response.message.content or ''
    except ollama.ResponseError as e:
        return f'Error: {e.error}'
    

def get_timestamp() -> str:
    """Return current timestamp as a string."""
    return datetime.datetime.now().replace(microsecond=0).isoformat()


def log(message: str, role: str, file_path: str):
    """Log a message with timestamp and role to the specified file."""
    with open(file_path, 'a') as f:
        f.write(f"[{get_timestamp()}] [{role}] {message}\n")

    if role != 'user':
        print(message)


def main():
    MODELS = ['gemma3:1b', 'gemma3:4b', 'gemma3:12b']
    CURRENT_MODEL = 'gemma3:1b'  # default small model
    TRANSCRIPTS_DIR = '../transcripts/'

    today = datetime.date.today()
    TRANSCRIPT_PATH = os.path.join(TRANSCRIPTS_DIR, str(today))
    os.makedirs(TRANSCRIPT_PATH, exist_ok=True)

    log_file_name = f'{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt' # format: YYYYMMDD_HHMMSS.txt
    log_file_path = os.path.join(TRANSCRIPT_PATH, log_file_name)

    print('Chatbot\n    /exit to quit\n    /new to clears in-memory history\n    /model <name> to switch models (gemma3:1b, gemma3:4b, gemma3:12b)\n')
    messages = []

    while True:
        user_input = input(">>>").strip()
        log(user_input, 'user', log_file_path)

        if user_input == '/exit': 
            output = 'Exiting...'
            log(output, 'system', log_file_path)
            break
        elif user_input == '/new': 
            messages = []
            output = 'In-memory history cleared'
            log(output, 'system', log_file_path)
            continue
        elif user_input.startswith('/model'):
            input_parts = user_input.split()
            if len(input_parts) != 2:
                output = f'Usage: /model <model_name> | Current model : {CURRENT_MODEL} | Available models: {MODELS})'
                log(output, 'system', log_file_path)
                continue

            model_name = input_parts[1] # get name
            if model_name in MODELS:
                CURRENT_MODEL = model_name
                output = f'Switched to model: {CURRENT_MODEL}'
                log(output, 'system', log_file_path)
            else:
                output = f'Model not recognized | Current model : {CURRENT_MODEL} | Available models: {MODELS}'
                log(output, 'system', log_file_path)
            continue

        messages.append({'role': 'user', 'content': user_input})        

        response = query_ollama(messages, CURRENT_MODEL)

        if response.startswith('Error:'):
            log(response, 'system', log_file_path)
        else:
            messages.append({'role': 'assistant', 'content': response})
            log(response, 'assistant', log_file_path)


if __name__ == "__main__":
    main()