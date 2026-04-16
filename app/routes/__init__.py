from flask import render_template, redirect, session, request


from app import app, db
from app.utils import login_required, validate_form
from app.validators import Registration
from app.db_models import User, Group, Membership, League, Game, Appearance