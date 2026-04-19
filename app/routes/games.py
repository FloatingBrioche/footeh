from flask import render_template, redirect, session, request

from app import app, db
from utils.decorators import login_required, validate_form
from app.db.models import User, Group, Membership, League, Game, Appearance


# <------------------------------------------------------ Games
@app.get("/games")
@login_required
def games_get():
    return render_template("games.html")
