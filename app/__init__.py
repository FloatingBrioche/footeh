
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv

import os

load_dotenv()

class Base(DeclarativeBase):
    pass

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.secret_key = os.getenv('SESSION_SECRET_KEY').encode()
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DATABASE_URL')
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_pre_ping": True, "echo": True}

db = SQLAlchemy(model_class=Base)
db.init_app(app)

from app import db_models, routes

with app.app_context():
    db.create_all()