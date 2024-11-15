import os
import json

from flask import Flask, request, jsonify
from crm import Crm
from tools import Tools
from openapi_def import OPENAPI_DEF

from dotenv import load_dotenv
load_dotenv()

from common.gpt import get_completion_with_tools, get_single_completion # type: ignore

app = Flask(__name__)
crm = Crm()
tools = Tools(crm)

# Laden Sie den geheimen Token aus einer Umgebungsvariable
RETOS_API_TOKEN = os.environ.get('RETOS_API_TOKEN')
if RETOS_API_TOKEN is None:
    raise ValueError('RETOS_API_TOKEN nicht in Umgebungsvariablen gefunden')

def is_valid_json(json_string):
    try:
        json.loads(json_string)
        return True
    except ValueError:
        return False    

@app.route('/schema', methods=['GET'])
def test():
    return OPENAPI_DEF, 200

@app.route('/crm/query', methods=['GET'])
def plain_text_query():
    # Prüfen, ob der Authorization-Header vorhanden ist und dem geheimen Token entspricht
    auth_header = request.headers.get('Authorization')
    if auth_header != RETOS_API_TOKEN:
        return jsonify({'message': 'Unauthorized'}), 401
    
    query = request.args.get('query')
    
    if not query:
        return jsonify({'message': 'Query parameter is required'}), 400

    try:
        messages=[{"role": "user", "content": query}]
        result = get_completion_with_tools(messages, tools)
        if is_valid_json(result):
            return result, 200
        else:
            return jsonify({"result": result}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500  # Fehlerbehandlung
    
# Catch-All Route
@app.route('/<path:subpath>', methods=['GET'])
def catch_all(subpath):
    print(f"Endpoint '{subpath}' not found.")
    return f"Endpoint '{subpath}' not found.", 404

if __name__ == '__main__':
    app.run(port=6000)
    
