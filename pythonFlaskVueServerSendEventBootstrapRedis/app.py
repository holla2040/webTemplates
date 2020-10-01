#!/usr/bin/env python3

import subprocess,os,time,json,redis
from Config import Config

config = Config()

from flask import Flask,Response
from flask import render_template

dbmq_client = redis.Redis(config.settings['dbmq_host'])

app = Flask(__name__)
opts = app.jinja_options.copy();
opts.update(dict(variable_start_string='^^', variable_end_string='^^'))
  # this de-confuses flask template replacement with vue's
app.jinja_options = opts
app.debug = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stream')
def stream():
   return Response(_stream(), content_type='text/event-stream')

@app.route('/logadd/<value>')
def logadd(value):
    dbmq_client.lpush(config.settings['dbmq_listkey'],"%s"%value)
    return Response("logadd %s"%value, mimetype='text/plain')

def _stream():
    while True:
        time.sleep(1.0)
        values = []
        list = dbmq_client.lrange(config.settings['dbmq_listkey'],0,-1)
        for v in list:
            values.append(v.decode('utf-8'))
        yield ("event: system\ndata: %s\n\n"%json.dumps({'tod':time.strftime("%y/%m/%d-%H:%M:%S",time.localtime()),'values':values}))


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,threaded=True)

