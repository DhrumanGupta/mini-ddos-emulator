from dotenv import load_dotenv
load_dotenv()

import os
import random
from time import sleep
from flask import Flask
import requests

app = Flask(__name__)

endpoints = ['/', '/endpoint-1', '/endpoint-2', '/endpoint-3']

def get_url(endpoint):
    return f"http://{os.getenv('SERVER_IP_ADDRESS')}{endpoint}"


def make_request_to_endpoint(endpoint):
    url = get_url(endpoint)
    print(f"Making request to {url}")
    requests.get(url)

@app.route('/emulate-user')
def normal():
    while True:
        make_request_to_endpoint(random.choice(endpoints))
        sleep(random.uniform(3, 5))
    return 'Hello world!'

@app.route('/emulate-malicious-user')
def malicous():
    while True:
        make_request_to_endpoint(random.choice(endpoints))
    return 'Hello world!'

@app.route('/')
def index():
    return 'pong'

app.run(host="0.0.0.0", port=80)