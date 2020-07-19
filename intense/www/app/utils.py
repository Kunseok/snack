import lwt
import sqlite3
from hashlib import sha256
from flask import g
from os import listdir, path
import datetime


DATABASE = "database.db"


class User:
    def __str__(self):
        return "User(username=%s,role=%d)" % (self.username,
                                              self.role)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def log_login(user):
    now = datetime.datetime.now()
    d = now.strftime("%Y-%m-%d")
    with open(f"logs/{d}.log", 'a') as log:
        log.write(str(user) + ' logged\n')


def badword_in_str(data):
    data = data.lower()
    badwords = ["rand", "system", "exec", "date"]
    for badword in badwords:
        if badword in data:
            return True
    return False


def hash_password(password):
    """ Hash password with a secure hashing function """
    return sha256(password.encode()).hexdigest()


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def get_user(username, secret):
    """ Returns User object if given username/secret exist in DB """
    username = username.decode()
    secret = secret.decode()
    res = query_db("select role from users where username = ? and secret = ?", (username, secret), one=True)
    if res:
        user = User()
        user.username = username
        user.role = res[0]
        log_login(user)
        return user
    return None

def try_login(form):
    """ Try to login with the submitted user info """
    if not form:
        return None
    username = form["username"]
    password = hash_password(form["password"])
    result = query_db("select count(*) from users where username = ? and secret = ?", (username, password), one=True)
    if result and result[0]:
        return {"username": username, "secret":password}
    return None


def get_session(request):
    """ Get user session and parse it """
    if not request.cookies:
        return 
    if "auth" not in request.cookies:
        return
    cookie = request.cookies.get("auth")
    try:
        info = lwt.parse_session(cookie)
    except lwt.InvalidSignature:
        return {"status": -1, "msg": "Invalid signature"}
    return info


def is_admin(request):
    session = get_session(request)
    if not session:
        return None
    if "username" not in session or "secret" not in session:
        return None
    user = get_user(session["username"], session["secret"])
    return user.role == 1


#### Logs functions ####
def admin_view_log(filename):
    if not path.exists(f"logs/{filename}"):
        return f"Can't find {filename}"
    with open(f"logs/{filename}") as out:
        return out.read()


def admin_list_log(logdir):
    if not path.exists(f"logs/{logdir}"):
        return f"Can't find {logdir}"
    return listdir(logdir)