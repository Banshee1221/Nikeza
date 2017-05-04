from parser import get_settings

from flask import Flask, request, render_template

app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py

session_vars = []

@app.route('/')
def index():
    # fake user
    return render_template('index.html',
                           title=get_settings()["general"]["sysname"],
                           username="Eugene")


@app.route('/', methods=["GET", "POST"])
def register():
    username = request.form['username']
    password = request.form['password']
    session_vars.append(username)
    session_vars.append(password)
    print(session_vars)
    return render_template('index.html',
                           title=get_settings()["general"]["sysname"],
                           username="Eugene")

app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.run(debug=True)