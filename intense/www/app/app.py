from flask import Flask, request, render_template, g, redirect, url_for,\
    make_response
from utils import get_db, get_session, get_user, try_login, query_db, badword_in_str
from admin import admin
import sqlite3
import lwt


app = Flask(__name__)

app.register_blueprint(admin)


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/submit', methods=["GET"])
def submit():
    session = get_session(request)
    if session:
        user = get_user(session["username"], session["secret"])
        return render_template("submit.html", page="submit", user=user)
    return render_template("submit.html", page="submit")


@app.route("/submitmessage", methods=["POST"])
def submitmessage():
    message = request.form.get("message", '')
    if len(message) > 140:
        return "message too long"
    if badword_in_str(message):
        return "forbidden word in message"
    # insert new message in DB
    try:
        query_db("insert into messages values ('%s')" % message)
    except sqlite3.Error as e:
        return str(e)
    return "OK"


@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html", page="login")


@app.route("/postlogin", methods=["POST"])
def postlogin():
    # return user's info if exists
    data = try_login(request.form)
    if data:
        resp = make_response("OK")
        # create new cookie session to authenticate user
        session = lwt.create_session(data)
        cookie = lwt.create_cookie(session)
        resp.set_cookie("auth", cookie)
        return resp
    return "Login failed"


@app.route("/logout")
def logout():
    resp = make_response("<script>document.location.href='/';</script>")
    resp.set_cookie("auth", "", expires=0)
    return resp


@app.route("/")
@app.route("/home")
def index():
    session = get_session(request)
    if session and "username" in session:
        user = get_user(session["username"], session["secret"])
        print(user)
        return render_template("home.html", page="home", user=user)
    return render_template("home.html", page="home")


if __name__ == "__main__":
    app.run()