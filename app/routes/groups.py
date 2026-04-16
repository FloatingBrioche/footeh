from app.routes import *

# <------------------------------------------------------ Groups
@app.get("/groups")
@login_required
def groups_get():
    return render_template("groups.html")


@app.get("groups/new")
@login_required
def groups_new_get():
    render_template("group_new.html")


@app.get("groups/join")
@login_required
def groups_new_get():
    render_template("group_join.html")