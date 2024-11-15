import os
import json
import uuid

from flask import Flask, request, jsonify
from crm import Crm
from todo import Todo
from tools import Tools
from tools_todo import ToolsTodo
from openapi_def import OPENAPI_DEF_CRM, OPENAPI_DEF_TODO
from preprocessing import preprocess
from dotenv import load_dotenv
load_dotenv()

from crm_logging import test_case_logger

from common.gpt import get_completion_with_tools, get_single_completion # type: ignore

app = Flask(__name__)
crm = Crm()
todo = Todo()
tools = Tools(crm)
tools_todo = ToolsTodo(todo)

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
    

@app.route('/crm', methods=['GET'])
def test():
    s = "<html><body><pre>"+OPENAPI_DEF_CRM+"\n\n"+OPENAPI_DEF_TODO+"</pre></body></html>"
    return s, 200

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
        request_id = str(uuid.uuid4())
        test_case_logger.info(f"{request_id} Received query: {query}")
        print(f"Received query: {query}")
        query = preprocess(query)
        print(f"Preprocessed query: {query}")
        test_case_logger.info(f"{request_id} Preprocessed query: {query}")
        messages=[{"role": "user", "content": query}]
        result = get_completion_with_tools(messages, tools, request_id)
        test_case_logger.info(f"{request_id} Final response: {result}")
        print(f"Final response: {result}")
        if is_valid_json(result):
            return result, 200
        else:
            return jsonify({"result": result}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500  # Fehlerbehandlung
    
@app.route('/crm/todos', methods=['GET'])
def todo_query():
    # Prüfen, ob der Authorization-Header vorhanden ist und dem geheimen Token entspricht
    auth_header = request.headers.get('Authorization')
    if auth_header != RETOS_API_TOKEN:
        return jsonify({'message': 'Unauthorized'}), 401
    
    query = request.args.get('query')
    
    if not query:
        return jsonify({'message': 'Query parameter is required'}), 400

    try:
        request_id = str(uuid.uuid4())
        print(f"{request_id} Received Todo query: {query}")
        messages=[{"role": "user", "content": query}]
        result = get_completion_with_tools(messages, tools_todo, request_id)
        print(f"{request_id} Final Todo Query response: {result}")
        if is_valid_json(result):
            return result, 200
        else:
            return jsonify({"result": result}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500  # Fehlerbehandlung
    
@app.route('/crm/testlogs', methods=['GET'])
def serve_test_logs():
    with open('test_cases.log', 'r') as f:
        return f.read(), 200


# Catch-All Route
@app.route('/<path:subpath>', methods=['GET'])
def catch_all(subpath):
    print(f"Endpoint '{subpath}' not found.")
    return f"Endpoint '{subpath}' not found.", 404

if __name__ == '__main__':
    app.run(port=6000)
    
