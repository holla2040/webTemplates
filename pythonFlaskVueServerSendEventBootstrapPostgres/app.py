#!/usr/bin/env python3

import subprocess,os,time,threading,json
from Config import Config

from psycopg2 import connect as db_connect

config = Config()

db_conn = db_connect("host='%s' user='%s' password='%s' dbname='%s'"%(config.settings['db_host'],config.settings['db_username'],config.settings['db_password'],config.settings['db_database']))
db_conn.autocommit = True
db_cur = db_conn.cursor()


values = []

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

@app.route('/logadd/<value>')
def logadd(value):
    body = '{"location":"dev","conditions":"dev","label":"dev","value":"%s"}'%value
    db_cur.execute("insert into %s(data) values ('%s')"%(config.settings['db_table'],body))
    return Response("logadd %s"%body, mimetype='text/plain')

def _stream():
    while True:
        time.sleep(1.0)
        db_cur.execute("select data->>'value' from %s where data->>'conditions' = 'dev' and data->>'location' = 'dev'"%config.settings['db_table'])
        values = []
        for v in db_cur.fetchall():
            values.append(v[0])
        yield ("event: system\ndata: %s\n\n"%json.dumps({'tod':time.strftime("%y/%m/%d-%H:%M:%S",time.localtime()),'values':values}))

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,threaded=True)

