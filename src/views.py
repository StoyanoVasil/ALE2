from flask import render_template, request, Response, json
from src import app

from src.models.InputParser import parse, parse_to_dfa
from src.models.RegexParser import parse_regex


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    args = parse(data['text'])
    return Response(json.dumps({'img': args[0], 'dfa': args[1], 'words': args[2],
                                'finite': args[3], 'possible_words': args[4]}))

@app.route('/regex', methods=['POST'])
def regex():
    data = request.json
    args = parse_regex(data['regex'])
    return Response(json.dumps({'img': args[0], 'dfa': args[1], 'words': args[2],
                                'finite': args[3], 'possible_words': args[4]}))

@app.route('/to-dfa', methods=['POST'])
def to_dfa():
    data = request.json
    args = parse_to_dfa(data['text'])
    return Response(json.dumps({'img': args[0], 'dfa': args[1], 'words': args[2],
                                'finite': args[3], 'possible_words': args[4]}))
