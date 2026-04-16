from app.routes import *

# <------------------------------------------------------ Groups
@app.get("/groups")
@login_required
def groups_get():
    return render_template("groups.html")