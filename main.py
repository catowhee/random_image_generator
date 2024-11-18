import os
import requests
import json
import random
import zmq
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
project_dir = Path(__file__).parent

def get_random_image(query):
    """
    https://unsplash.com/documentation#get-a-random-photo
    """
    url = f"https://api.unsplash.com/photos/random?query={query}"
    headers = {
        "Authorization": f"Client-ID {os.getenv("ACCESS_KEY")}"
    } 
    r = requests.get(url, headers=headers)

    if r.status_code == 200:
        try:
            image = json.loads(r.content)
        except:
            return get_fallback_image()
        else:
            store_image(image)
            return image
    else:
        return get_fallback_image()
        
        
def store_image(image):
    with open(f"{project_dir}/fallback_store.json", "r+", encoding="utf-8") as infile:
        content = infile.read()
        if content.strip() == "[]" or content.strip() == "":
            store = []
        else:
            infile.seek(0)
            store = json.load(infile)
        # Store a max of 500 images
        if len(store) < 500:
            store.append(image)
            infile.seek(0)
            infile.truncate()
            json.dump(store, infile)


def get_fallback_image():
    with open(f"{project_dir}/fallback_store.json", "r", encoding="utf-8") as infile:
        try:
            store = json.load(infile)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None
        else:
            rando = random.randint(0, len(store) - 1)
            return store[rando]

print(get_random_image("ice cream"))