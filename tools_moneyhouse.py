import json
import logging
import os

from moneyhouse import Moneyhouse

login = os.environ.get('MONEYHOUSE_LOGIN')
password = os.environ.get('MONEYHOUSE_PASSWORD')

class ToolsMoneyhouse:
    def __init__(self, moneyhouse: Moneyhouse):
        self.moneyhouse = moneyhouse

    def search_moneyhouse(self, query):
        try:
            result = self.moneyhouse.search_moneyhouse(query)
            result = json.dumps(result)
            print(result)
        except Exception as e:
            logging.error("Error in search_moneyhouse: "+str(e))
            return json.dumps({"error": str(e)})
        
        return result
    
    def get_moneyhouse_company_info(self, url):
        try:
            result = self.moneyhouse.get_moneyhouse_company_info(url) 
            result = json.dumps(result)
            print(result)
        except Exception as e:
            logging.error("Error in search_moneyhouse: "+str(e))
            return json.dumps({"error": str(e)})
        
        return result
      
    def get_tools(self):
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "search_moneyhouse",
                    "description": "Search for companies with a given name. Returns a list of objects with name and url of the company",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "Query": {
                                "type": "string",
                                "description": "Name of the company"
                            },
                         },
                        "required": ["Query"]
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_moneyhouse_company_info",
                    "description": "Get information about a company from Moneyhouse. Returns an object like { 'alter_der_firma': '37 Jahre', 'umsatz': '1-10 Mio.', 'groesse': '20-49', 'status': 'aktiv' }",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "Url": {
                                "type": "string",
                                "description": "Url of the company"
                            },
                         },
                        "required": ["Url"]
                    },
                }
            }]
        return tools
    
    def call_function(self, function_name, function_to_call, function_args):
        if function_name == "search_moneyhouse":
            function_response = function_to_call(
                query=function_args.get("Query")
            )
        elif function_name == "get_moneyhouse_company_info":
            function_response = function_to_call(
                url=function_args.get("Url")
            )
        else:
            print("Function not found: ", function_name)
            function_response = json.dumps({"error": "function not found: "+function_name})
        return function_response

    def handle_tool_call(self, tool_call, messages, request_id = None):
        if not tool_call:
            return None
        
        available_functions = {
            "search_moneyhouse": self.search_moneyhouse,
            "get_moneyhouse_company_info": self.get_moneyhouse_company_info,
        }  

        function_name = tool_call.function.name
        function_to_call = available_functions[function_name]
        try:
            function_args = json.loads(tool_call.function.arguments)
        except Exception as e:
            function_args = {}
            error = str(e)
            print("Error: ", e)

        function_response = self.call_function(function_name, function_to_call, function_args)
        
        messages.append(
            {
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": function_response
            }
        )  # extend conversation with function response


