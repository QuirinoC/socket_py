from flask import Flask, jsonify, make_response, request, render_template, Response
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

slaves = [
    '127.0.0.2',
    '127.0.0.3',
    '127.0.0.4',
]

@app.route('/', methods=['GET'])
def root():
    return 'ok'