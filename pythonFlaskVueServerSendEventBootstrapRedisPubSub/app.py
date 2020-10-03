#!/usr/bin/env python3

import subprocess,os,time,json,redis
from Config import Config

config = Config()

from flask import Flask,Response
from flask import render_template

dbmq_client = redis.Redis(config.settings['dbmq_host'])
pubsub = dbmq_client.pubsub()
pubsub.subscribe('event')

app = Flask(__name__)
opts = app.jinja_options.copy();
opts.update(dict(variable_start_string='^^', variable_end_string='^^'))
  # this de-confuses flask template replacement with vue's
app.jinja_options = opts

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stream')
def stream():
   return Response(_stream(), content_type='text/event-stream')

def _stream():
  timeout = 0
  while True:
    event = pubsub.get_message() 
    if event:
      try:
        data = event['data'].decode()
        yield ("event: system\ndata: %s\n\n"%json.dumps({'event':data}))
      except:
        # sometimes data isn't byte array
        pass
      # print(repr(data).decode())
    if time.time() > timeout:
      yield ("event: system\ndata: %s\n\n"%json.dumps({'tod':time.strftime("%y/%m/%d-%H:%M:%S",time.localtime())}))
      timeout = time.time() + 1.0


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,threaded=True)

