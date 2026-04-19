from app import db
from app.db.models import Membership, Group


def add_user(user):
    db.session.add(user)
    db.session.commit()
    return user.id


def add_group(group: Group, user_id):
    db.session.add(group)
    new_membership = Membership(
        user_id=user_id,
        group_id=group.id,
        role="organiser",
    )
    db.session.add(new_membership)
    db.session.commit()

