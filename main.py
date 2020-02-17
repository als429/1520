# starting example from https://github.com/timothyrjames/cs1520/blob/master/week04/gae/project2/main.py

from flask import Flask, redirect, render_template

app = Flask(__name__)

@app.route('/')
def root():
    return render_template('/index.html')

if __name__ == '__main__':
        app.run(host='127.0.0.1', port=8020, debug=True) # updated port, so that when it runs locally, it runs on 8020
