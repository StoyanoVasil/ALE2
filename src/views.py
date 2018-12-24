from flask import render_template, request, Response, json
from src import app

from src.models.temp import parse


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    args = parse(data['text'])
    return Response(json.dumps({'img': args[0], 'dfa': args[1], 'words': args[2],
                                'finite': args[3], 'possible_words': args[4]}))

