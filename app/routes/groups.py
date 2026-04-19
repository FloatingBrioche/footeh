from flask import render_template, redirect, session, request

from app import app
from utils.decorators import login_required, validate_form
from utils.validators import NewGroup
from app.db.models import Group
from app.db.input import add_group
from app.db.output import get_groups


# <------------------------------------------------------ Groups
@app.get("/groups")
@login_required
def groups_get():
    users_groups = get_groups(session["user_id"])
    return render_template("groups.html", groups=users_groups)


@app.post("/groups")
@login_required
@validate_form(validator=NewGroup, template="groups_new.html")
def groups_post(new_group_data: NewGroup):
    new_group = Group(**new_group_data.model_dump())
    add_group(new_group, session["user_id"])
    app.logger.info(
        "Created new group: %s (ID: %d)",
        new_group.name,
        new_group.id,
    )
    app.logger.info(
        "Added user ID %d as admin to group ID %d",
        session["user_id"],
        new_group.id,
    )
    return redirect("/groups")


@app.get("/groups/new")
@login_required
def groups_new_get():
    render_template("group_new.html")


@app.get("/groups/join")
@login_required
def groups_join_get():
    render_template("group_join.html")
