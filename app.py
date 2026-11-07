from flask import Flask, render_template, request, redirect, url_for
from account_stuff import handleLogin, validateAccount

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")
@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == "GET":
        return render_template('login.html',title="Login")
    elif request.method == "POST":
        handleLogin(request)
        return redirect(url_for("index"))
@app.route("/register", methods=['GET','POST'])
def register():
    if request.method == "GET":
        return render_template('register.html', title="Register")
    elif request.method == "POST":
        validateAccount(request)
        return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
