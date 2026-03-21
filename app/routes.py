from flask import render_template, redirect, session

from app import app



# <------------------------------------------------------ Home
@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


# <------------------------------------------------------ Register, Login, Logout
@app.route("/register", methods=["GET"])
def register_get():
    if "user_id" in session:
        return redirect("/")
    else:
        return render_template("signup.html")


@app.route("/register", methods=["POST"])
def register_post():
    # Handle registration logic here
    pass

@app.route("/login", methods=["GET"])
def login_get():
    if "user_id" in session:
        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/logout", methods=["GET"])
def logout_get():
    session.clear()
    return redirect("/")


# <------------------------------------------------------ Account
@app.route("/account", methods=["GET"])
def account_get():
    return render_template("account.html")


# <------------------------------------------------------ Games
@app.route("/games", methods=["GET"])
def games_get():
    return render_template("games.html")


# <------------------------------------------------------ Groups
@app.route("/groups", methods=["GET"])
def groups_get():
    return render_template("groups.html")