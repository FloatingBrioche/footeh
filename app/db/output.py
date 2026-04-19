from app import db
from app.db.models import User

def get_user(email: str):
    user = db.session.execute(
        db.select(User).filter_by(email=email)
    ).scalar_one_or_none()
    return user