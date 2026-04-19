import os

from flask import Flask
from dotenv import load_dotenv
import click

from app.db import models


load_dotenv()


# Initialize Flask app
app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.secret_key = os.getenv("SESSION_SECRET_KEY").encode()

# Database configuration & initialization
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_pre_ping": True, "echo": False}
db = models.db
db.init_app(app)

with app.app_context():
    db.create_all()


@click.command("update-db-schema")
def update_db_schema():
    
    """Initialize the database."""
    db.drop_all()
    db.create_all()
    click.echo("DB schema updated.")

app.cli.add_command(update_db_schema)


# Import routes after app and db are initialized to avoid circular imports
from app.routes import account, games, groups, home


