import os

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session, abort, flash
from helperfunctions.account_stuff import handleLogin, createNewAccount
from helperfunctions.advent import getAdventDays
from helperfunctions.leetcodeAPI import pickAProblem, solvedRecently
from helperfunctions.progress import getCompletedDays, getUserData, assignProblem, markDayCompleted

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
    days = getAdventDays(completed=getCompletedDays(session["username"]))
    return render_template("index.html", days=days, year=days[0]["date"].year)
@app.route("/day/<int:n>")
def day(n):
    if not 1 <= n <= 25:
        abort(404)
    userStuff = getUserData(session["username"])
    completed = set(userStuff.get("completed_days", []))
    info = getAdventDays(completed=completed)[n - 1]
    # no peeking at future days by typing the URL (checked before using any API calls)
    if not info["unlocked"]:
        return redirect(url_for("index"))

    # keep the same problem once a day has one; only pick for unassigned, unfinished days
    assigned = userStuff.get("assigned", {})
    slug = assigned.get(str(n))
    if slug is None and n not in completed:
        problem = pickAProblem(userStuff.get("leetcode_username", ""), assigned)
        if problem is not None:
            slug = problem["titleSlug"]
            assignProblem(session["username"], n, slug)

    return render_template("day.html", title=f"Day {n}", day=info, problem_slug=slug)
@app.route("/day/<int:n>/check", methods=["POST"])
def check_day(n):
    # "Check Submission" button: look for the assigned problem in the user's 20 most recent LeetCode solves
    if not 1 <= n <= 25:
        abort(404)
    userStuff = getUserData(session["username"])
    completed = set(userStuff.get("completed_days", []))
    info = getAdventDays(completed=completed)[n - 1]
    if not info["unlocked"]:
        return redirect(url_for("index"))
    if info["completed"]:
        return redirect(url_for("day", n=n))

    slug = userStuff.get("assigned", {}).get(str(n))
    if slug is None:
        flash("This day doesn't have a problem yet. Refresh the page to get one.", "error")
        return redirect(url_for("day", n=n))

    result = solvedRecently(userStuff.get("leetcode_username", ""), slug)
    if result is None:
        flash("Couldn't reach LeetCode right now. Try again in a minute.", "error")
    elif result:
        markDayCompleted(session["username"], n)
        flash(f"Day {n} complete! 🎁", "success")
    else:
        flash("Not found in your 20 most recent accepted submissions. "
              "If you just submitted, wait a few minutes and check again.", "error")
    return redirect(url_for("day", n=n))
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
