from flask import render_template, redirect, session, request
from werkzeug.security import check_password_hash


from app import app, db
from app.utils import login_required, validate_form
from app.validators import Registration
from app.db_models import User, Group, Membership, League, Game, Appearance


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
    new_user = User(**registration_data.model_dump(exclude={"__pydantic_extra__"}))
    db.session.add(new_user)
    db.session.commit()
    session["user_id"] = new_user.id
    session["first_name"] = new_user.first_name
    session["last_name"] = new_user.last_name
    session["email"] = new_user.email
    return redirect("/groups")


@app.route("/login", methods=["GET"])
def login_get():
    if "user_id" in session:
        return redirect("/games")
    else:
        return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    
    user = db.session.execute(db.select(User).filter_by(email=email)).scalar_one_or_none()
    
    if not user:
        error_message = "Invalid email. There's no account associated with that email address."
        return render_template("login.html", error=error_message)

    if not check_password_hash(user.password_hash, password):
        error_message = "Invalid password."
        return render_template("login.html", error=error_message)
    
    session["user_id"] = user.id
    session["first_name"] = user.first_name
    session["last_name"] = user.last_name
    session["email"] = user.email
    
    return redirect("/games")


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