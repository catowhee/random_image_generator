## Overview ##
The microservice accepts a keyword query, uses the Unsplash API to find a random image, and returns a JSON object with the image info.

The API account you'll make for Unsplash will be in demo mode, which means it's limited to 50 requests per hour. To prevent disruptions, the microservice stores the last 500 images in `fallback_store.json` and returns a random image from this file if there are API errors stemming from rate limits or anything else.

Note, this file is empty until a successfull API call is made. 

## Communication policy ##

#### How to programatically REQUEST data ####
Use Python's ZeroMQ package to communicate with the microservice.
Create a request socket and bind it to tcp://localhost:5555. Use the send_string method to initiate a search:
```python
socket.send_string("icecream")
```

#### How to programatically RECEIVE data ####
Use the recv() method. The microservice will return a JSON object with details about a single random image.
```python
ice_cream_json = socket.recv()
```

## Setup ##

#### Unsplash API ####

The microservice uses the Unsplash API to retrieve images. An API account is required to use it. Follow these steps:

1. Go to the [Unsplash Developer Page](https://unsplash.com/developers).
2. Create an account if you don’t have one.
3. Register a new application and copy your **Access Key**.

#### .env  ####

Create a `.env` file and add your access key:

```dotenv
    ACCESS_KEY=your_access_kewy
```

#### Dependencies ####
To install the required packages, use the following command:

```bash
pip install -r requirements.txt
```

![UML](uml.jpeg)

