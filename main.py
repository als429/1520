from flask import Flask, redirect, render_template, Response
import json # for backend sign in functionality

import f_data # includes our data classes: User, Dinner, Food, Location
import f_datastore

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
    file = '/index.html'
    title = 'Food with Friends: Eat up!'
    h1 = 'Eat Leftovers'
    return show_page(file,title,h1)
	
@app.route('/cook')
def cook():
    file = '/cook.html'
    title = 'Cook for Friends'
    h1 = 'Cook'
    return show_page(file,title,h1)
	
@app.route('/host')
def host():
    file = '/host.html'
    title = 'Host a Dinner & Make Friends'
    h1 = "Host"
    return show_page(file,title,h1)
	
@app.route('/attend')
def attend():
    file = '/attend.html'
    title = 'Attend a Dinner & Make Friends'
    h1 ="Attend"
    return show_page(file,title,h1)

# currently has location code from James
# testing if user is pulling in from datastore
# and populating in the HTML
# Not workkkking.....
@app.route('/eat-list') 
def eatlist():
    food_code = 'Food01'
    log('before loading from ds')
    food = f_datastore.load_food(food_code)
    log('after loading from ds')
    return show_page('/eat-list.html',food=food) 

# backend sign in functionality	
@app.route('/authtoken', methods=['POST'])
def authtoken():
    log('Token: ' + request.form.get('token'))
    d = { 'message': 'Auth Token received at server.' }
    return Response(json.dumps(d), mimetype='application/json')

# utility function that allows us to 
# consolidate on the render_template function
# will allow us to expand on parameters, as week04/gae/project2/main
# start to get user, location, food, and dinner data
def show_page(page, title, h1, user=None, location=None, 
			  food=None, dinner=None, errors=None):
	return render_template(page, 
			       page_title=title, #on-page = parameter
			       h1=h1,
				   user=user, # may need to replace with like a flask.session.get('user', None) or something
				   location=location,
				   food=food,
				   dinner=dinner,
			       errors=errors)

# We should only use this to populate our data for the first time.
@app.route('/createdata')
def createdata():
    f_datastore.create_data()
    return 'OK'

#@app.route('/test') # currently testing templates
#def test():
#    return render_template('test.html', page_title='Testing Templates!!!-uyfuar',h1="blah")

if __name__ == '__main__':
        app.run(host='127.0.0.1', port=8082, debug=True) # updated port, so that when it runs locally, it runs on 8030
