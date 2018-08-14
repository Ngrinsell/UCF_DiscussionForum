from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *
from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os, bcrypt, datetime, json, html
 
app = Flask(__name__)
 
# Endpoint to render the homepage. If the user is logged in show them the forum, if not get them to log in
@app.route('/')
def home():
    if not session.get('logged_in'):
        session['logged_in'] = False
        return render_template('login.html')
    else:
        return render_template('home.html')

# Endpoint that "logs out" users, by setting their session attributes back to defaults
@app.route('/logout')
def logout():
    session['username'] = ""
    session['logged_in'] = False
    return home()

# Endpoint to allow users to log in
@app.route('/login', methods=['POST'])
def login():
    Session = sessionmaker(bind=engine)
    s = Session()
    username = html.escape(request.form['username'])
    query = s.query(User).filter(User.username.in_([username])).first()
    if bcrypt.hashpw(html.escape(request.form['password']).encode('utf8'), query.salt.encode('utf8')) == query.password:
        session['logged_in'] = True
        session['username'] = query.username
    else:
        return(notFound)
    return home()

# Endpoint for those who go to register, handles if they are already logged in
@app.route('/register')
def renderRegister():
    if not session.get('logged_in'):
        return render_template('register.html')
    else:
        return "You are already logged in."

# Register new user, then redirect back home
@app.route('/register', methods=['POST'])
def register():
    shaker = bcrypt.gensalt()
    uname = html.escape(request.form['username'])
    pword = html.escape(request.form['password']).encode('utf8')
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([uname]))
    result = query.first()
    if result:
        return "Error, username already taken."
    salt = bcrypt.gensalt()
    user = User(uname,bcrypt.hashpw(pword, salt), salt)
    s.add(user)
    s.commit()
    s.commit()
    session['logged_in'] = True
    session['username'] = uname
    return "You are now registered and logged in.  <script>window.location = '/';</script>"

# Endpoint to return a json object containing all posts to be displayed. If user isn't authenticated return nothing
@app.route('/getPosts', methods=['POST'])
def getPosts():
    if not session.get('logged_in'):
        session['logged_in'] = False    
    if (session['logged_in'] == True):
        file = open('post.json', 'a+')
        dirtylaundy = file.read()
        if len(dirtylaundy) > 0:
            threads = json.loads(dirtylaundy)   
        else:
            threads = []
        numthreads = len(threads)
        file.close()
        return json.dumps(threads) 
    else:
        return json.dumps([])  

# Endpoint that handles a new post/reply
@app.route('/post', methods=['POST'])
def reply():
    if(session['logged_in'] == True):
        submitPost(int(html.escape(request.form['threadId'])), html.escape(session['username']), html.escape(request.form['topic']), html.escape(request.form['body']))
    return home()

# Handles posting content to our forum, and appending to the json file
def submitPost(di, usr, tpc, bidy):
    file = open('post.json', 'a+')
    dirtylaundy = file.read()
    if len(dirtylaundy) > 0:
        threads = json.loads(dirtylaundy)   
    else:
        threads = []
    numthreads = len(threads)
    file.close()
    if (di == -1):
        new = {"id" : numthreads, "topic": tpc, "reply": []}
        numthreads += 1
        newr = {"username": usr, "body": bidy, "timestamp" : datetime.datetime.now().strftime("%m-%d %H:%M")}
        new['reply'].append(newr)
        threads.append(new)
        with open('post.json', 'w') as outfile:
            outfile.write(json.dumps(threads))
    else:
        newr = {"username" : usr, "body": bidy, "timestamp" : datetime.datetime.now().strftime("%m-%d %H:%M")}
        threads[di]['reply'].append(newr)
        with open('post.json', 'w') as outfile:
            outfile.write(json.dumps(threads))

# Error handlers, for security pourposes we're not giving anything away to external users. 
@app.errorhandler(403)
def notFound(error):
    return notFound

@app.errorhandler(404)
def notFound(error):
    return notFound

@app.errorhandler(405)
def notFound(error):
    return notFound

@app.errorhandler(500)
def notFound(error):
    return notFound

@app.errorhandler(502)
def notFound(error):
    return notFound

@app.errorhandler(503)
def notFound(error):
    return notFound

# On startup or import, create webserver and set constant responses
# If this is not a production server, change debug to true, and preferably the port number to something > 3000
notFound = "Not found. <script>window.location = '/';</script>"
app.secret_key = os.urandom(12)
app.run(debug=False,host='0.0.0.0', port=80)
