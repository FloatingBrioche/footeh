from app import db
from app.db.models import Membership, Group, User


def add_user(user: User):
    db.session.add(user)
    db.session.commit()
    return user.id


def add_group(group: Group, user_id: int):
    db.session.add(group)
    db.session.commit()
    membership = Membership(
        user_id=user_id,
        group_id=group.id,
        role="organiser",
    )
    add_membership(membership)


def add_membership(membership: Membership):
    db.session.add(membership)
    db.session.commit()

