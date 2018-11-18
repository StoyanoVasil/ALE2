from src import app


@app.route('/')
def index():
    return 'Hello ALE2'
