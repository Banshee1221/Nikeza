from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py

@app.route('/')
@app.route('/index')
def index():
    # fake user
    return render_template('index.html',
                           title='Home',
                           username="Eugene")

app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.run(debug=True)