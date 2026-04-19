from app.routes import *


# <------------------------------------------------------ Groups
@app.get("/groups")
@login_required
def groups_get():
    stmt = (
        db.select(Group.__table__, Membership.role)
        .join(Membership, Group.id == Membership.group_id)
        .where(
            Membership.user_id == session["user_id"],
            Membership.status == "active",
            Group.status == "active",
        )
    )
    users_groups = db.session.execute(stmt).scalars().all()

    return render_template("groups.html", groups=users_groups)


@app.post("/groups")
@login_required
@validate_form(validator=NewGroup, template="groups_new.html")
def groups_post(new_group_data: NewGroup):
    new_group = Group(**new_group_data.model_dump())
    db.session.add(new_group)
    new_membership = Membership(
        user_id=session["user_id"],
        group_id=new_group.id,
        role="organiser",
    )
    db.session.add(new_membership)
    db.session.commit()
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
