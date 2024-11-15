import json
from crm import Crm

class Tools:
    def __init__(self, crm: Crm):
        self.crm = crm

    def get_crm_data(self, sql_query):
        try:
            result = self.crm.get_data(sql_query) 
        except Exception as e:
            return json.dumps({"error": str(e)})
        
        return result

    def get_tools(self):
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_crm_data",
                    "description": "Query the CRM data",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": """
Perform SQL queries on the table 'organizations'.
The organizations table has the following fields:
Organisationsname,Webseite,"Umsatz (MIO CHF)","Distanz ZH (km)",zuständig,"Distanz Chur (km)","primäre E-Mail",Branche,Rechnungsadresse,"Rechnung PLZ","Rechnung Postfach","Rechnung Ort","Rechnung Land","Klassifizierung Softwareentwicklung und -testing ","Klassifizierung Prüfsysteme","Klassifizierung AI (Künstliche Intelligenz)","Klassifizierung Azure","Klassifizierung Traineeprogramm","Klassifizierung swissICT Booster 50+",Typ,Beschreibung,Unternehmenszweck,Verwaltungsrat,Zeichnungsberechtigte,Kundenart"
""",
                            }
                        },
                        "required": ["query"]
                    },
                }
            }]
        return tools
    
    def call_function(self, function_name, function_to_call, function_args):
        if function_name == "get_crm_data":
            function_response = function_to_call(
                sql_query=function_args.get("query")
            )
        else:
            print("Function not found: ", function_name)
            function_response = json.dumps({"error": "function not found: "+function_name})
        return function_response

    def handle_tool_call(self, tool_call, messages):
        error = False
        if not tool_call:
            return None
        
        available_functions = {
            "get_crm_data": self.get_crm_data
        }  

        function_name = tool_call.function.name
        function_to_call = available_functions[function_name]
        try:
            function_args = json.loads(tool_call.function.arguments)
        except Exception as e:
            function_args = {}
            error = str(e)
            print("Error: ", e)

        print("Calling function: ", function_name, " with args: ", function_args)

        function_response = self.call_function(function_name, function_to_call, function_args)
        
        messages.append(
            {
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": function_response
            }
        )  # extend conversation with function response


