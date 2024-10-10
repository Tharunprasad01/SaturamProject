import sqlite3
from flask import Flask,request,jsonify,make_response,session,redirect
import jwt
import datetime
from functools import wraps
app = Flask(__name__)

app.config['SECRET_KEY']='THISisTHEsecretKEY'
token_blacklist = set()

def connectDb():
     conn = sqlite3.connect('UserAuthenticationSystem.db')
     return conn

@app.route('/')
def home():
    if not session.get('loggedin'):
        return redirect('/login')
    else:
        return "Logged in "

def tokenReqd(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'Message':'Token is Missing'}),403
        if token in token_blacklist:
            return jsonify({'Message':'Token has been logged out'})
        try:
            data = jwt.decode(token,app.config['SECRET_KEY'],algorithms=["HS256"])
            if not data.get("status"):
                return redirect('/')
        except jwt.ExpiredSignatureError:
            return jsonify({'Message':'Token has expired'}),403
        except jwt.InvalidTokenError:
            return jsonify({'Message':'Invalid Token'}),403
        return f(*args,**kwargs)
    return decorated

@app.route('/unprotected')
def unProtected():
    return jsonify({'Message':'Anyone can view This'})

@app.route('/protected')
@tokenReqd
def protected():
    return jsonify({'Message':'This is only for people with valid tokens'})

@app.route('/login')
def login():
    name = request.args.get('username')
    password = request.args.get('password')
    a = connectDb()
    c = a.cursor()
    auth=c.execute("Select password from Users where name = ?",(name,)).fetchone()
    print(auth)
    if auth and password == auth[0]:
        session['loggedin']=True
        token = jwt.encode(
                {'user':name,'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=10),'status':True},app.config['SECRET_KEY'])
        session["token"] = token
        return jsonify({'token':token})
    return make_response('Could not verify !',401,{'WWW-Authenticate':'Basic realm="Login Reqd"'})

@app.route('/logout')
def logout():
    token = request.args.get('token')
    token_blacklist.add(token)
    data = jwt.decode(token,app.config["SECRET_KEY"],algorithms=["HS256"])
    name = data["user"]
    session['loggedin'] = False
    logout1 = jwt.encode(
                {'user':name,'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=10),'status':False},app.config['SECRET_KEY'])
    return jsonify({'Message':'Successfully logged out'})


if __name__ == '__main__':
    app.run(debug=True)