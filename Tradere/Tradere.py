from os import urandom
from parser import get_settings

import operations
from flask import Flask, request, render_template, session, g, redirect, url_for

app = Flask(__name__)
app.config.from_object(__name__)
app.config['CACHE_TYPE'] = 'simple'
app.secret_key = urandom(24)


@app.before_request
def before_request():
    g.error = False
    g.user = None
    g.password = None
    if 'user' in session and 'password' in session:
        g.user = session['user']
        g.password = session['password']


@app.route('/', methods=["GET", "POST"])
def index():
    if g.user:
        return redirect(url_for('queue'))
    if request.method == 'POST':
        session.pop('user', None)
        print(request.form['username'], request.form['password'])
        if request.form['username'] != '' or request.form['password'] != '':
            session['user'] = request.form['username']
            session['password'] = request.form['password']
            return redirect(url_for('queue'))
        else:
            g.error = True

    return render_template('index.html',
                           title=get_settings()["general"]["sysname"],
                           plugin_image="static/images/{0}".format(get_settings()["backend"]["platform_image"]),
                           error=g.error)


@app.route('/getsession')
def getsession():
    if 'user' in session:
        return session['user']
    return "Not logged in"


@app.route('/queue')
def queue():
    if g.user:
        operation = operations.Ops(g.user, g.password)
        operation.get_queue()
        return render_template("queue.html",
                               title=get_settings()["general"]["sysname"])
    return redirect(url_for("index"))


@app.route('/new')
def new():
    if g.user:
        return render_template("new.html",
                               title=get_settings()["general"]["sysname"])
    return redirect(url_for("index"))



@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))


app.run(debug=True, host="0.0.0.0", port=5432)
