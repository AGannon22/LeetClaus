import os

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session, abort
from helperfunctions.account_stuff import handleLogin, createNewAccount
from helperfunctions.advent import getAdventDays

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]

PUBLIC_ENDPOINTS = {"login", "register", "static"}


@app.before_request
def require_login():
    if request.endpoint not in PUBLIC_ENDPOINTS and "username" not in session:
        return redirect(url_for("login"))
@app.route("/")
def index():
    days = getAdventDays()
    return render_template("index.html", days=days, year=days[0]["date"].year)
@app.route("/day/<int:n>")
def day(n):
    if not 1 <= n <= 25:
        abort(404)
    info = getAdventDays()[n - 1]
    # no peeking at future days by typing the URL
    if not info["unlocked"]:
        return redirect(url_for("index"))
    return render_template("day.html", title=f"Day {n}", day=info)
@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == "GET":
        if "username" in session:
            return redirect(url_for("index"))
        return render_template('login.html',title="Login")
    elif request.method == "POST":
        result = handleLogin(request)
        if result != 'passed':
            return render_template('login.html', title="Login", error=result), 401
        else:
            session.clear()
            session["username"] = request.form["username"]
            return redirect(url_for("index"))
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))
@app.route("/register", methods=['GET','POST'])
def register():
    if request.method == "GET":
        return render_template('register.html', title="Register")
    elif request.method == "POST":
        result = createNewAccount(request)
        if result != "passed":
            # show the form again with the error in a pop-up
            return render_template('register.html', title="Register", error=result), 400
        return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
