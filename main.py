import os
import requests
import json
import random
import zmq
import time
from dotenv import load_dotenv
from pathlib import Path

# Load the .env data
load_dotenv()

# Get the project dir. We'll use this to locate fallback_store.json
project_dir = Path(__file__).parent

def get_random_image(query):
    """
    Retrieves a random image from the unsplash API
    API documentation: https://unsplash.com/documentation#get-a-random-photo
    """
     
    url = f"https://api.unsplash.com/photos/random?query={query}"
    headers = {
        "Authorization": f"Client-ID {os.getenv("ACCESS_KEY")}"
    } 

    # Make the API call
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Something went wrong with the Unsplash API call:\n{e}")
        return get_fallback_image()
    
    # Attempt to load JSON
    try:
        image = json.loads(r.content)
    except Exception as e:
        print(f"Unexpected response from Unsplash:\n{e}\n")
        return get_fallback_image()
    else:
        print("API call succesfull!")
        store_image(image)
        return image
    
        
def store_image(image):
    """
    Saves the API response to fallback_store.json
    """

    with open(f"{project_dir}/fallback_store.json", "r+", encoding="utf-8") as infile:
        content = infile.read()
        if content.strip() == "[]" or content.strip() == "":
            store = []
        else:
            infile.seek(0)
            store = json.load(infile)

        # Insert new image
        store.insert(0, image)

        # Store a max of 500 images
        if len(store) > 500:
            store.pop()

        # Write to file    
        infile.seek(0)
        infile.truncate()
        json.dump(store, infile)

def get_fallback_image():
    """
    Retrieve an image from fallback_store.json
    """

    print("Attempting to retrieve fallback image from fallback_store.json...")
    with open(f"{project_dir}/fallback_store.json", "r", encoding="utf-8") as infile:
        try:
            store = json.load(infile)
        except Exception as e:
            print(f"An error occured while retrieving the fallback image:\n{e}\nThis may mean fallback_store.json is empty because a successfull API response hasn't been stored.")
            return None
        else:
            rando = random.randint(0, len(store) - 1)
            print("Retrieved a fallback image...")
            return store[rando]


# Server
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    message = socket.recv()
    print(f"Received request from the client: {message.decode()}")
    if len(message) > 0:
        if message.decode() == 'Q': # Client asked server to quit
            break
        else:
            image = get_random_image(message.decode())
            socket.send_string(json.dumps(image))
context.destroy()
