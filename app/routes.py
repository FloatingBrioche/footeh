from app import app

@app.route('/')
@app.route('/index')
def index():
    return "Fancy a game of footeh?"