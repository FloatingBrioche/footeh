from werkzeug.security import check_password_hash
from flask import render_template, redirect, session, request

from app import app
from utils.decorators import login_required, validate_form
from utils.validators import Registration
from app.db.models import User
from app.db.input import add_user
from app.db.output import get_user


# <------------------------------------------------------ Register
@app.get("/register")
def register_get():
    if "user_id" in session:
        return redirect("/")
    else:
        return render_template("register.html")


@app.post("/register")
@validate_form(validator=Registration, template="register.html")
def register_post(registration_data: Registration):
    new_user = User(**registration_data.model_dump())
    add_user(new_user)
    app.logger.info(
        "Registered new user: %s %s (ID: %d)",
        new_user.first_name,
        new_user.last_name,
        new_user.id,
    )
    session["user_id"] = new_user.id
    session["first_name"] = new_user.first_name
    session["last_name"] = new_user.last_name
    session["email"] = new_user.email
    return redirect("/groups")


# <------------------------------------------------------ Login
@app.get("/login")
def login_get():
    if "user_id" in session:
        return redirect("/games")
    else:
        return render_template("login.html")


@app.post("/login")
def login_post():
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    user = get_user(email)

    if not user:
        error_message = (
            "Invalid email. There's no account associated with that email address."
        )
        return render_template("login.html", error=error_message)

    if not check_password_hash(user.password_hash, password):
        error_message = "Invalid password."
        return render_template("login.html", error=error_message)

    session["user_id"] = user.id
    session["first_name"] = user.first_name
    session["last_name"] = user.last_name
    session["email"] = user.email

    return redirect("/games")


# <------------------------------------------------------ Logout
@app.route("/logout", methods=["GET"])
def logout_get():
    session.clear()
    return redirect("/")


# <------------------------------------------------------ Account
@app.get("/account")
@login_required
def account_get():
    return render_template("account.html")
