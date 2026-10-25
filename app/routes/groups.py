from flask import render_template, redirect, session, request

from app import app
from app.utils.decorators import login_required, validate_form
from app.utils.validators import NewGroup
from app.db.models import Group
from app.db.input import add_group
from app.db.output import get_groups


# <------------------------------------------------------ View
@app.get("/groups")
@login_required
def groups_get():
    users_groups = get_groups(session["user_id"])
    return render_template("groups.html", groups=users_groups)

@app.get("/groups/<int:group_id>")
@login_required
def group_get(group_id: int):
    group = Group.query.get_or_404(group_id)
    return render_template("group.html", group=group)


# <------------------------------------------------------ Create
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


@app.get("/groups/create")
@login_required
def groups_create_get():
    return render_template("groups/create.html")

# <------------------------------------------------------ Join
@app.get("/groups/join")
def groups_join_code_get():
    join_code = request.args.get("join_code")
    if join_code:
        group = Group.query.filter_by(join_code=join_code).first()
        if group:
            return redirect(f"/groups/join/{group.id}")
        else:
            return render_template("groups/join_code.html", error="Invalid join code.")
    return render_template("groups/join_code.html")


@app.get("/groups/join/<int:group_id>")
@login_required
def groups_join_get_post(group_id: int):
    group = Group.query.get_or_404(group_id)
    return render_template("groups/join.html", group=group)


@app.post("/groups/join/<int:group_id>")
@login_required
def groups_join_post(group_id: int):
    group = Group.query.get_or_404(group_id)
    return redirect(f"/groups/{group_id}")

