from flask import Flask, jsonify, make_response, request, render_template, Response
from flask_cors import CORS
import os
from optparse import OptionParser
import json
app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def root():
    return 'ok'

@app.route('/get_files', methods=['GET'])
def get_files():
    files = '\n'.join(os.listdir())
    return str(files)

@app.route('/get_file',methods=['GET'])
def get_file():
    file_name = request.args.get('file_name')
    with open(file_name,'r') as file:
        return file.read()

@app.route('/create_file',methods=['POST'])
def create_file():
        file_name = json.loads(request.data)['file_name']
        text      = json.loads(request.data)['text']
        with open(file_name,'w') as file:
                file.write(text)
        return 'ok'

if __name__ == '__main__':
    parser = OptionParser()
    args = parser.parse_args()
    #print(get_file('master.py'))
    
    app.run(host=args[1][0],port='80',debug=True)