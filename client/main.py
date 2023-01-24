import threading
from dotenv import load_dotenv
load_dotenv()

import os
import random
import time
from time import sleep
from flask import Flask, request
import requests

app = Flask(__name__)

user_endpoints = ['/', '/endpoint-1', '/endpoint-2', '/endpoint-3']
malicious_endpoints = ['/endpoint-3', '/endpoint-4', '/endpoint-5']

def get_url(endpoint):
    return f"http://{os.getenv('SERVER_IP_ADDRESS')}{endpoint}"


def make_request_to_endpoint(endpoint):
    url = get_url(endpoint)
    print(f"Making request to {url}")
    requests.get(url)

user_thread: threading.Thread = None
user_running = False

malicious_thread: threading.Thread = None
malicious_running = False

def run_user(timetorun):
    global user_running
    start = time.time()
    while start + timetorun > time.time():
        if not user_running:
            break
        make_request_to_endpoint(random.choice(user_endpoints))
        sleep(random.uniform(3, 5))
    user_running = False

def run_malicious(timetorun):
    global malicious_running
    start = time.time()
    while start + timetorun > time.time():
        if not malicious_running:
            break
        make_request_to_endpoint(random.choice(malicious_endpoints))
    malicious_running = False

@app.route('/emulate-user')
def normal():
    global user_thread, user_running
    args = request.args
    timetorun = args.get("time", default=0, type=int)
    if timetorun <= 1:
        return "Invalid time"

    if user_thread:
        return "User already running"
    
    user_running = True
    user_thread = threading.Thread(target=run_user, args=(timetorun,))
    user_thread.start()

    # start = time.time()

    return 'Hello world!'

@app.route('/stop-user')
def stop_user():
    global user_thread, user_running
    if user_thread:
        user_running = False
        user_thread.join()
        del user_thread
        user_thread = None
        return "User stopped"
    else:
        return "No user running"

@app.route('/emulate-malicious-user')
def malicous():
    global malicious_thread, malicious_running

    args = request.args
    timetorun = args.get("time", default=0, type=int)
    if timetorun <= 1:
        return "Invalid time"

    if malicious_thread:
        return "malicious already running"
    
    malicious_running = True
    malicious_thread = threading.Thread(target=run_malicious, args=(timetorun,))
    malicious_thread.start()

    return 'Hello world!'

@app.route('/stop-malicious-user')
def stop_malicious():
    global malicious_thread, malicious_running
    if malicious_thread:
        malicious_running = False
        malicious_thread.join()
        del malicious_thread
        malicious_thread = None
        return "User stopped"
    else:
        return "No malicious user running"


@app.route('/')
def index():
    return 'pong'

app.run(host="0.0.0.0", port=80)