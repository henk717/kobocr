import time
import base64
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import requests
import os

import configparser

config = configparser.ConfigParser()

# Lets make the default config if it does not exist
def write_config():
    config.write(open('config.cfg', 'w'))

if not os.path.exists('config.cfg'):
    config['config'] = {'kcpp_url': 'http://127.0.0.1:5001', 'path_to_watch': 'input'}
    write_config()
    if not os.path.exists("input"): 
        os.makedirs("input")

config.read_file(open(r'config.cfg'))
ENDPOINT = config.get('config', 'kcpp_url')
path_to_watch = config.get('config', 'path_to_watch')

if not os.path.exists("output"): 
    os.makedirs("output") 

if not os.path.exists("prompt.txt"): 
    with open("prompt.txt", 'w', encoding='utf-8') as file:
        file.write("Output only the text in the image.")


class NewFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            with open(event.src_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                input_filename = os.path.splitext(os.path.basename(event.src_path))[0]
                ai_processing(encoded_string, input_filename)

def ai_processing(base64, input_filename):
    with open("prompt.txt", "r", encoding="utf-8") as prompt_file:
        prompt = prompt_file.read().replace('\n', '')
        input_json = {
            "prompt": f"{{[INPUT]}}{prompt}{{[OUTPUT]}}",
            "images": [base64],
            "max_context_length": 8192, # How much of the prompt will we submit to the AI generator? (Prevents AI / memory overloading)
            "max_length": 512, # How long should the response be?
            "temperature": 0.1, # Make it focused 
            "replace_instruct_placeholders": "True", # Make the placeholders work in all formats
            "quiet": "False" # Don't print what you are doing in the KoboldAI console, helps with user privacy
        }
        print(input_json)
        response = requests.post(f"{ENDPOINT}/api/v1/generate", json=input_json)
        if response.status_code == 200:
            results = response.json()['results']
            text = results[0]['text']
            response_text = text.split('\n')[0].replace("  ", " ")
            print(text)
            with open(os.path.join(os.path.curdir, 'output', input_filename), 'w', encoding='utf-8') as file:
                file.write(text)
        else:
            print(response)

if __name__ == "__main__":
    event_handler = NewFileHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path_to_watch, recursive=False)
    observer.start()

    try:
        print(f"Watching for new image files in: {path_to_watch}")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
