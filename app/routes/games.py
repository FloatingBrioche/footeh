from app.routes import *

# <------------------------------------------------------ Games
@app.get("/games")
@login_required
def games_get():
    return render_template("games.html")