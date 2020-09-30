#!/usr/bin/env python3

import subprocess,os,time,threading,json
from Config import Config

config = Config()

from flask import Flask,Response
from flask import render_template

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

def _stream():
    while True:
        time.sleep(1.0)
        yield ("event: system\ndata: %s\n\n"%json.dumps({'tod':time.strftime("%y/%m/%d-%H:%M:%S",time.localtime())}))


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)

