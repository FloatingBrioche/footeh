from flask import render_template, redirect, session, request
from werkzeug.security import check_password_hash


from app import app
from app.utils import login_required, validate_form
from app.validators import Registration


# <------------------------------------------------------ Home
@app.route('/')
@app.route('/index')
def index():
    if "user_id" in session:
        return redirect("/games")
    
    return render_template("index.html")


# <------------------------------------------------------ Register, Login, Logout
@app.route("/register", methods=["GET"])
def register_get():
    if "user_id" in session:
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/register", methods=["POST"])
@validate_form(validator=Registration, template="register.html")
def register_post(registration_data: Registration):
    pass


@app.route("/login", methods=["GET"])
def login_get():
    if "user_id" in session:
        return redirect("/games")
    else:
        return render_template("login.html")


@app.route("/logout", methods=["GET"])
def logout_get():
    session.clear()
    return redirect("/")


# <------------------------------------------------------ Account

@app.route("/account", methods=["GET"])
@login_required
def account_get():
    return render_template("account.html")


# <------------------------------------------------------ Games
@app.route("/games", methods=["GET"])
@login_required
def games_get():
    return render_template("games.html")


# <------------------------------------------------------ Groups
@app.route("/groups", methods=["GET"])
@login_required
def groups_get():
    return render_template("groups.html")