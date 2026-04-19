from app import db
from app.db.models import Group, Membership, User


def get_user(email: str):
    user = db.session.execute(
        db.select(User).filter_by(email=email)
    ).scalar_one_or_none()
    return user


def get_groups(user_id):
    stmt = (
        db.select(Group.__table__, Membership.role)
        .join(Membership, Group.id == Membership.group_id)
        .where(
            Membership.user_id == user_id,
            Membership.status == "active",
            Group.status == "active",
        )
    )
    users_groups = db.session.execute(stmt).scalars().all()
    return users_groups