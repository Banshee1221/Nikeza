from os import urandom
from parser import get_settings
import json
import operations
from flask import Flask, request, render_template, session, g, redirect, url_for, jsonify

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
    if request.args.get('error'):
        g.error = True
    if g.user and not g.error:
        return redirect(url_for('queue'))
    if request.method == 'POST':
        session.pop('user', None)
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


@app.route('/queue', methods=['GET', 'POST'])
def queue():
    if request.method == 'POST':
        print((request.get_json()))
    if g.user:
        try:
            operation = operations.Ops(g.user, g.password)
        except Exception:
            return redirect(url_for("index", error=True))
        return render_template("queue.html",
                               title=get_settings()["general"]["sysname"],
                               queue_dict=operation.get_queue())
    return redirect(url_for("index", error=True))


@app.route('/_updateQueue', methods=['GET'])
def updateQueue():
    if g.user:
        try:
            operation = operations.Ops(g.user, g.password)
        except Exception:
            return redirect(url_for("index", error=True))
        return jsonify(j=operation.get_queue())
    return redirect(url_for("index", error=True))


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
