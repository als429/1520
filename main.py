# starting example from https://github.com/timothyrjames/cs1520/blob/master/week04/gae/project2/main.py

from flask import Flask, redirect, render_template
import json # for backend sign in functionality

app = Flask(__name__)

@app.route('/')
@app.route('/index.html')
def root():
    return render_template('/index.html')

@app.route('/eat')
def eat_list():
    return render_template('/index.html')
	
@app.route('/cook')
def cook():
    return render_template('/cook.html')
	
@app.route('/host')
def host():
    return render_template('/host.html')
	
@app.route('/attend')
def attend():
    return render_template('/attend.html')

@app.route('/eat-list')
def eatlist():
	return render_template('/eat-list.html')


# backend sign in functionality
def log(msg):
    """Log a simple message."""
    # Look at: https://console.cloud.google.com/logs to see your logs.
    # Make sure you have "stdout" selected.
    print('main: %s' % msg)
	
@app.route('/authtoken', methods=['POST'])
def authtoken():
    log('Token: ' + request.form.get('token'))
    d = {
        'message': 'Auth Token received at server.',
    }
    return flask.Response(json.dumps(d), mimetype='application/json')

if __name__ == '__main__':
        app.run(host='127.0.0.1', port=8080, debug=True) # updated port, so that when it runs locally, it runs on 8080
