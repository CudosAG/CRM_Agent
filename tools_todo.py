import json
import logging
from crm_logging import test_case_logger
from crm import Crm
from todo import Todo

class ToolsTodo:
    def __init__(self, todo: Todo):
        self.todo = todo

    def get_todo_data(self, sql_query):
        try:
            result = self.todo.query_todos(sql_query) 
            result = result.to_markdown()
            print(result)
        except Exception as e:
            logging.error("Error in get_todo_data: "+str(e))
            return json.dumps({"error": str(e)})
        
        return result
    
    def add_todo_data(self, name, firma, notiz, deadline):
        try:
            result = self.todo.add_todo(name, firma, notiz, deadline)
        except Exception as e:
            logging.error("Error in add_todo_data: "+str(e))
            return json.dumps({"error": str(e)})
        
        return result
    
    def delete_todo_data(self, index):
        try:
            result = self.todo.delete_todo(index)
        except Exception as e:
            logging.error("Error in delete_todo: "+str(e))
            return json.dumps({"error": str(e)})
        
        return result

    
    def get_tools(self):
        tools = [

            {
                "type": "function",
                "function": {
                    "name": "get_todo_data",
                    "description": "Query the todo data",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": """
Gib deine SQL-Abfrage ein (z.B. SELECT * FROM todos WHERE Firma='XYZ')
Felder sind Id, Name, Firma, Notiz, Deadline.
""",
                            }
                        },
                        "required": ["query"]
                    },
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "add_todo_data",
                    "description": "Add todo data",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "Name": {
                                "type": "string",
                                "description": "Name des Users"
                            },
                            "Firma": {
                                "type": "string",
                                "description": "Firma mit der man etwas zu tun hat"
                            },
                            "Notiz": {
                                "type": "string",
                                "description": "Notiz zum Todo"
                            },
                            "Deadline": {
                                "type": "string",
                                "description": "Deadline des Todos"
                            }
                        },
                        "required": ["Name", "Firma", "Notiz", "Deadline"]
                    },
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_todo_data",
                    "description": "Delete todo data",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "id des zu löschenden Todos"
                            }
                        },
                        "required": ["index"]
                    },
                }
            }]
        return tools
    
    def call_function(self, function_name, function_to_call, function_args):
        if function_name == "get_todo_data":
            function_response = function_to_call(
                sql_query=function_args.get("query")
            )
        elif function_name == "add_todo_data":
            function_response = function_to_call(
                name=function_args.get("Name"),
                firma=function_args.get("Firma"),
                notiz=function_args.get("Notiz"),
                deadline=function_args.get("Deadline")
            )
        elif function_name == "delete_todo_data":
            function_response = function_to_call(
                index=function_args.get("index")
            )
        else:
            print("Function not found: ", function_name)
            function_response = json.dumps({"error": "function not found: "+function_name})
        return function_response

    def handle_tool_call(self, tool_call, messages, request_id = None):
        error = False
        if not tool_call:
            return None
        
        available_functions = {
            "get_todo_data": self.get_todo_data,
            "add_todo_data": self.add_todo_data,
            "delete_todo_data": self.delete_todo_data
        }  

        function_name = tool_call.function.name
        function_to_call = available_functions[function_name]
        try:
            function_args = json.loads(tool_call.function.arguments)
        except Exception as e:
            function_args = {}
            error = str(e)
            print("Error: ", e)

        test_case_logger.info(f"{request_id} Calling function: {function_name} with args: {function_args}")
        function_response = self.call_function(function_name, function_to_call, function_args)
        
        messages.append(
            {
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": function_response
            }
        )  # extend conversation with function response


