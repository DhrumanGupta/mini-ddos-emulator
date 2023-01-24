from datetime import datetime, timedelta
import random
import time
from flask import Flask, request
import pandas as pd
import os
from queue import Queue

app = Flask(__name__)
data_queue = Queue()

columns = ['ip', 'endpoint', 'packet_size', 'headers', 'time', 'time_taken']
data = pd.DataFrame(columns=columns)
i = 0
filename = f"data_{i}.csv"
while os.path.exists(filename):
    i += 1
    filename = f"data_{i}.csv"

route_data = {
    "/": {
        "packet_size": [30, 100],
        "time_taken": [0.01, 0.1]
    },
    "/endpoint-1": {
        "packet_size": [250, 500],
        "time_taken": [0.03, 0.2]
    },
        "/endpoint-2": {
        "packet_size": [250, 500],
        "time_taken": [0.05, 0.15]
    },
    "/endpoint-3": {
        "packet_size": [500, 1000],
        "time_taken": [0.04, 0.15]
    },
    "/endpoint-4": {
        "packet_size": [3000, 6000],
        "time_taken": [0.1, 0.3]
    },
    "/endpoint-5": {
        "packet_size": [5000, 9700],
        "time_taken": [0.1, 0.37]
    },
}

@app.before_request
def log_request_info():
    # print(str(request.get_data()))
    # data.loc[len(data)] = [request.remote_addr, request.path, request.method, request.get_data(), request.headers, time.time()]
    # df.append(df({
    #     "ip": request.remote_addr,
    #     "endpoint": request.path,
    #     "method": request.method,
    #     # "body": str(request.get_data()),
    #     # "headers": str(request.headers),
    #     "time": time.time()
    # }))

    if request.path not in route_data.keys():
        return

    req_data = route_data[request.path]

    packet_size = random.randint(req_data["packet_size"][0], req_data["packet_size"][1])
    time_taken = random.uniform(req_data["time_taken"][0], req_data["time_taken"][1])

    data_queue.put([request.remote_addr, request.path, packet_size, request.headers, time.time(), time_taken])
    if len(data) % 100 == 0:
        data.to_csv(filename, index=False)
    # app.logger.debug('Body: %s', request.get_data())

@app.route('/')
def hello_world():
    return 'Hello world!'

@app.route('/endpoint-1')
def hello_world_1():
    return 'Hello world!'

@app.route('/endpoint-2')
def hello_world_2():
    return 'Hello world!'

@app.route('/endpoint-3')
def hello_world_3():
    return 'Hello world!'

@app.route('/endpoint-4')
def hello_world_4():
    return 'Hello world!'

@app.route('/endpoint-5')
def hello_world_5():
    return 'Hello world!'


def save_logs():
    global data
    while True:
        # start = datetime.now()
        end = datetime.now() + timedelta(seconds=1)
        res = []
        while datetime.now() < end:
            try: 
                new_data = data_queue.get(timeout=0.1)
                res.append(new_data)
            except:
                continue

        res_df = pd.DataFrame.from_records(res, columns=columns)
        data = pd.concat([data, res_df])
        # print(data)
        data.to_csv(filename, index=False)

if __name__ == "__main__":
    import threading
    t = threading.Thread(target=save_logs, daemon=True)
    t.start()
    app.run(host='0.0.0.0', port=80)

    
