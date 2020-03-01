# starting example from https://github.com/timothyrjames/cs1520/blob/master/week04/gae/project2/main.py

from flask import Flask, redirect, render_template, Response
import json # for backend sign in functionality

from google.oauth2 import id_token
from google.auth.transport import requests

app = Flask(__name__)

# logging to console
def log(msg):
    """Log a simple message."""
    # Look at: https://console.cloud.google.com/logs to see your logs.
    # Make sure you have "stdout" selected.
    print('main: %s' % msg)
	
# app routing
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

@app.route('/test')
def test():
    return render_template('test.html', page_title='test Page')

# backend sign in functionality	
@app.route('/authtoken', methods=['POST'])
def authtoken():
    log('Token: ' + request.form.get('token'))
    d = { 'message': 'Auth Token received at server.' }
	# (Receive token by HTTPS POST)
	# ...

    try:
		# Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)

		# Or, if multiple clients access the backend server:
		# idinfo = id_token.verify_oauth2_token(token, requests.Request())
		# if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
		#     raise ValueError('Could not verify audience.')
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')

		# If auth request is from a G Suite domain:
		# if idinfo['hd'] != GSUITE_DOMAIN_NAME:
		#     raise ValueError('Wrong hosted domain.')

		# ID token is valid. Get the user's Google Account ID from the decoded token.
        userid = idinfo['sub']
    except ValueError:
		# Invalid token
        pass
    return Response(json.dumps(d), mimetype='application/json')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True) # updated port, so that when it runs locally, it runs on 8080
