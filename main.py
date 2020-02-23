# starting example from https://github.com/timothyrjames/cs1520/blob/master/week04/gae/project2/main.py

from flask import Flask, redirect, render_template

app = Flask(__name__)

@app.route('/')
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

if __name__ == '__main__':
        app.run(host='127.0.0.1', port=8030, debug=True) # updated port, so that when it runs locally, it runs on 8030
