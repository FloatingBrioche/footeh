from app.routes import *

# <------------------------------------------------------ Groups
@app.get("/groups")
@login_required
def groups_get():
    return render_template("groups.html")


@app.post("/groups")
@login_required
@validate_form(validator=NewGroup, template="groups_new.html")
def groups_post():
    return render_template("groups.html")


@app.get("/groups/new")
@login_required
def groups_new_get():
    render_template("group_new.html")


@app.get("/groups/join")
@login_required
def groups_join_get():
    render_template("group_join.html")