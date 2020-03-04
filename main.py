# starting example from https://github.com/timothyrjames/cs1520/blob/master/week04/gae/project2/main.py

from flask import Flask, redirect, render_template, Response
import json # for backend sign in functionality

app = Flask(__name__)

# logging to console
def log(msg):
    """Log a simple message."""
    # Look at: https://console.cloud.google.com/logs to see your logs.
    # Make sure you have "stdout" selected.
    print('main: %s' % msg)
	
# app routing
@app.route('/')
@app.route('/eat')
@app.route('/index.html')
def root():
    return render_template('/index.html',page_title='Food with Friends: Eat up!')
	
@app.route('/cook')
def cook():
    return render_template('/cook.html',page_title='Cook for Friends')
	
@app.route('/host')
def host():
    return render_template('/host.html',page_title='Host a Dinner & Make Friends')
	
@app.route('/attend')
def attend():
    return render_template('/attend.html',page_title='Attend a Dinner & Make Friends')

@app.route('/eat-list')
def eatlist():
    return render_template('/eat-list.html') # currently has location code from James

@app.route('/test')
def test():
    return render_template('test.html', page_title='Testing Templates!!!-uyfuar')

# backend sign in functionality	
@app.route('/authtoken', methods=['POST'])
def authtoken():
    log('Token: ' + request.form.get('token'))
    d = { 'message': 'Auth Token received at server.' }
    return Response(json.dumps(d), mimetype='application/json')
	

if __name__ == '__main__':
        app.run(host='127.0.0.1', port=8082, debug=True) # updated port, so that when it runs locally, it runs on 8030