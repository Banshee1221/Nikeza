from os import urandom
from parser import get_settings
import json
import operations
from flask import Flask, request, render_template, session, g, redirect, url_for, jsonify

app = Flask(__name__)
app.config.from_object(__name__)
app.config['CACHE_TYPE'] = 'simple'
app.secret_key = ':\xe1\xfd\xa0n\xec\xe5\xb8\xb4\x95+\xcd\xce\x81\xe7\x99\xd4\xb9\xa7$\xc3\xf5e\x9a'

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
    if request.args.get('error') and 'user' in session:
        g.error = True
        session.pop('user', None)
    if g.user and not g.error:
        return redirect(url_for('queue'))
    if request.method == 'POST':
        session.pop('user', None)
        if request.form['username'] != '' or request.form['password'] != '':
            session['user'] = request.form['username']
            session['password'] = request.form['password']
            session['requestCont'] = ""
            return redirect(url_for('queue'))
        else:
            g.error = True
            session.pop('user', None)

    return render_template('index.html',
                           title=get_settings()["general"]["sysname"],
                           plugin_image="static/images/{0}".format(get_settings()["backend"]["platform_image"]),
                           error=g.error)


@app.route('/getsession')
def getsession():
    if 'user' in session:
        return session
    return "Not logged in"


@app.route('/queue', methods=['GET', 'POST'])
def queue():
    if g.user:
        try:
            operation = operations.Ops(g.user, g.password)
            if request.method == 'POST':
                print((request.get_json()))
                operation.stop_run(request.get_json())
        except Exception as e:
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


@app.route('/new', methods=['GET', 'POST'])
def new():
    if g.user:
        try:
            operation = operations.Ops(g.user, g.password)
            if request.method == 'POST':
                print("!!"+str(request.get_json()).strip())
                session['requestCont'] = str(request.get_json()).strip()
                session.modified = True
        except Exception as e:
            return redirect(url_for("index", error=True))
        return render_template("new.html",
                               title=get_settings()["general"]["sysname"],
                               initData=operation.get_storage())
    return redirect(url_for("index"))


@app.route('/_new', methods=['POST', 'GET'])
def updateTree():
    if g.user:
        try:
            operation = operations.Ops(g.user, g.password)
            if 'id' in request.args:
                if request.args.get('id') != "root":
                    return jsonify(operation.get_storage_inner(request.args.get('id')))
        except Exception as e:
            print("well oops :/", e)
            return ""
        print("!!"+session['requestCont'])
        return jsonify(operation.get_storage())
    return redirect(url_for("index", error=True))



@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))


app.run(debug=True, host="0.0.0.0", port=5432)
