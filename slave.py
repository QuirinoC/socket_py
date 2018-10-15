from flask import Flask, jsonify, make_response, request, render_template, Response
from flask_cors import CORS
import os
app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def root():
    return 'ok'

@app.route('/get_files', methods=['GET'])
def get_files():
    files = '\n'.join(os.listdir())
    return str(files)

if __name__ == '__main__':
    app.run(host='127.0.0.2',port='80',debug=True)