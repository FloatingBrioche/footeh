from flask import render_template, redirect, session, request

from app import app

# <------------------------------------------------------ Home
@app.route("/")
@app.route("/index")
def index():
    if "user_id" in session:
        return redirect("/games")

    return render_template("index.html")
