import logging
from parser import get_settings
import uuid
import operations
from flask import Flask, request, render_template, session, g, redirect, url_for, jsonify


app = Flask(__name__)
app.config.from_object(__name__)
app.config['CACHE_TYPE'] = 'simple'
app.secret_key = ':\xe1\xfd\xa0n\xec\xe5\xb8\xb4\x95+\xcd\xce\x81\xe7\x99\xd4\xb9\xa7$\xc3\xf5e\x9a'

@app.before_request
def before_request():
    """
    Sets initial variables on first request
    :return: None
    """
    g.error = False
    g.user = None
    g.password = None
    if 'user' in session and 'password' in session and 'tenant' in session:
        g.user = session['user']
        g.password = session['password']
        g.tenant = session['tenant']


@app.route('/', methods=["GET", "POST"])
def index():
    """
    The main/default route of the application. Presents user with login screen
    :return: render_template('index.html') if user not logged in
    :return: redirect(url_for('queue')) if user logged in
    """
    app.logger.info("\n=== index()/ ===")
    if request.args.get('error') and 'user' in session:
        app.logger.error("E:Error on login")
        g.error = True
        session.pop('user', None)
    if g.user and not g.error:
        app.logger.info("I:User logged in, redirecting to queue")
        return redirect(url_for('queue'))
    if request.method == 'POST':
        session.pop('user', None)
        if request.form['username'] != '' or request.form['password'] != '' or request.form['tenant'] != '':
            app.logger.info("I:Setting user information for session")
            session['user'] = request.form['username']
            session['password'] = request.form['password']
            session['tenant'] = request.form['tenant']
            session['id'] = uuid.uuid4()
            session['requestCont'] = ""
            session['file'] = None
            session['other'] = ""
            app.logger.info("I:Redirecting user to queue")
            print(session['user'], session['password'], session['tenant'])
            return redirect(url_for('queue'))
        else:
            app.logger.error("E:Error logging user in")
            g.error = True
            session.pop('user', None)
    app.logger.info("I:Rendering main index template")
    return render_template('index.html',
                           title=get_settings()["general"]["sysname"],
                           plugin_image="static/images/{0}".format(get_settings()["backend"]["platform_image"]),
                           error=g.error)


@app.route('/getsession')
def getsession():
    """
    Debug route to display session information
    :return: User details if logged in
    :return: Error string if not logged in
    """
    if 'user' in session:
        response = "User: {0} | Password: {1} | Session: {2} | Cookie: {3}" \
                   "".format(session['user'], session['password'], session['id'], request.cookies['session'])
        return response
    return "Not logged in"


@app.route('/queue', methods=['GET', 'POST'])
def queue():
    app.logger.info("\n=== queue()/queue ===")
    if g.user:
        app.logger.info("I:Attempt login check...")
        try:
            operation = operations.Ops(g.user, g.password, g.tenant)
            if request.method == 'POST':
                app.logger.info("I:POST received -> stop_run()")
                app.logger.info("I:Received json from ajax - " + str(request.get_json()))
                operation.stop_run(request.get_json())
        except Exception as e:
            app.logger.error("E:Issue stopping server -> " + str(e))
            return redirect(url_for("index", error=True))
        app.logger.info("I:Sending user to queue")
        return render_template("queue.html",
                               title=get_settings()["general"]["sysname"],
                               queue_dict=operation.get_queue())
    app.logger.error("E:User not signed in! Redirect")
    return redirect(url_for("index", error=True))


@app.route('/_updateQueue', methods=['GET'])
def updateQueue():
    app.logger.info("=== updateQueue()/_updateQueue ===")
    if g.user:
        app.logger.info("I:Attempting login check...")
        try:
            operation = operations.Ops(g.user, g.password, g.tenant)
        except Exception as e:
            app.logger.error("E:Could not log user in to backend -> " + str(e))
            return redirect(url_for("index", error=True))
        app.logger.info("I:Getting queue from backend")
        return jsonify(j=operation.get_queue())
    return redirect(url_for("index", error=True))


@app.route('/new', methods=['GET', 'POST'])
def new():
    app.logger.info("=== new()/new ===")
    if g.user:
        app.logger.info("I:Attempting login check...")
        try:
            operation = operations.Ops(g.user, g.password, g.tenant)
            if request.method == 'POST':
                app.logger.info("I:POST received")
                app.logger.info("I:Get new page request -> "+str(request.get_json()).strip())
                session['requestCont'] = str(request.get_json()).strip()
                session.modified = True
        except Exception as e:
            app.logger.error("E:Could not log user in to backend -> " + str(e))
            return redirect(url_for("index", error=True))
        app.logger.info("I:Get storage data from get_storage()")
        storageData = operation.get_storage()
        app.logger.info("I: Storage data -> "+str(storageData))
        return render_template("new.html",
                               title=get_settings()["general"]["sysname"],
                               initData=storageData,
                               initData2=storageData)
    app.logger.error("E:User not logged in! Redirecting")
    return redirect(url_for("index"))


@app.route('/_new', methods=['POST', 'GET'])
def updateTree():
    app.logger.info("=== updateTree()/_new ===")
    if g.user:
        app.logger.info("I:Attempting login check...")
        try:
            operation = operations.Ops(g.user, g.password, g.tenant)
            app.logger.info("I:POST received -> "+str(request.args))
            if 'id' in request.args:
                if request.args.get('id') != "root":
                    return jsonify(operation.get_storage_inner(request.args.get('id')))
        except Exception as e:
            app.logger.error("E: Could not receive storage information -> " + str(e))
            return ""
        app.logger.info("I:RequestConf variable -> "+str(session['requestCont']))
        return jsonify(operation.get_storage())
    app.logger.error("E:User not logged in! Redirecting")
    return redirect(url_for("index", error=True))

@app.route('/_upload', methods=['POST'])
def upload():
    app.logger.info("=== upload()/_upload ===")
    if g.user:
        app.logger.info("I:Attempting login check...")
        try:
            if request.get_json() is not None:
                session['other'] = request.get_json()
                app.logger.info("I:POST received, 'other' -> " + str(session['other']))
            if len(request.files) > 0:
                app.logger.info("I:POST received, file upload")
                request.files['file'].save("runtime/{0}".format(session['other']['cwlFileName']))
                operation = operations.Ops(g.user, g.password, g.tenant)
                app.logger.info("I:Creating script for starting instance")
                operation.create_script(session['id'], session['other']['cwlFileName'], session['other'], request.cookies['session'], g.user, g.password)
        except Exception as e:
            app.logger.error("E:Could not start new instance in backend -> " + str(e))
            return ""
        return "success"
    app.logger.error("E:User not logged in! Redirecting")
    return redirect(url_for("index", error=True))

@app.route('/_done', methods=['POST'])
def jobDone():
    app.logger.info("=== jobDone()/_done ===")
    app.logger.info("+++ Virtual machine requesting shutdown")
    if g.user:
        app.logger.info("I:Attemtping login check...")
        try:
            operation = operations.Ops(g.user, g.password, g.tenant)
            if request.method == 'POST':
                response = request.get_json()
                app.logger.info("I:POST received, uuid of instance -> " + str(response['uuid']))
                response_proc = ""
                try:
                    response_proc = str(response['uuid'].decode()).strip()
                except:
                    response_proc = str(response['uuid']).strip()
                app.logger.info("I:Attempting to stop instance")
                operation.stop_run([response_proc])
        except Exception as e:
            app.logger.error("E:Could not stop instance -> " + str(e))
            return ""
        return "success"
    app.logger.error("E:User not logged in! Redirecting")
    return redirect(url_for("index", error=True))


@app.route('/logout')
def logout():
    app.logger.info("=== logout/logout ===")
    app.logger.info("I:Removing user session")
    session.pop('user', None)
    return redirect(url_for('index'))


app.run(debug=True, host="0.0.0.0", port=5432)
