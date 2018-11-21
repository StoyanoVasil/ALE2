from flask import render_template, request, Response, json
from src import app

from src.models.temp import parse


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    name, is_dfa = parse(data['text'])
    return Response(json.dumps({'img': name, 'dfa': is_dfa}))
