# starting example from https://github.com/timothyrjames/cs1520/blob/master/week04/gae/project2/main.py

from flask import Flask, redirect

app = Flask(__name__)

@app.route('/')
def root():
    return redirect("/s/index.html", code=302)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8050, debug=True) # updated port, so that when it runs locally, it runs on 8050
