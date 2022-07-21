import time
from flask import Flask, request
import json
from pandas import DataFrame as df

app = Flask(__name__)

data = df(columns=['ip', 'endpoint', 'method', 'body', 'headers', 'time'])

@app.before_request
def log_request_info():
    # print(str(request.get_data()))
    data.loc[len(data)] = [request.remote_addr, request.path, request.method, request.get_data(), request.headers, time.time()]
    # df.append(df({
    #     "ip": request.remote_addr,
    #     "endpoint": request.path,
    #     "method": request.method,
    #     # "body": str(request.get_data()),
    #     # "headers": str(request.headers),
    #     "time": time.time()
    # }))
    if len(data) % 100 == 0:
        data.to_csv('data.csv', index=False)
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

app.run(host='192.168.1.17')