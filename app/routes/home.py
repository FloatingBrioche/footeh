from app.routes import *

# <------------------------------------------------------ Home
@app.route("/")
@app.route("/index")
def index():
    if "user_id" in session:
        return redirect("/games")

    return render_template("index.html")