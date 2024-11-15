import json
import logging
from crm_logging import test_case_logger
from crm import Crm

class Tools:
    def __init__(self, crm: Crm):
        self.crm = crm

    def get_crm_data(self, sql_query):
        try:
            result = self.crm.get_data(sql_query) 
        except Exception as e:
            logging.error("Error in get_crm_data: "+str(e))
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
Führe SQL Queries auf der Datenbank aus. Die Datenbank enthält Informationen über Organisationen, Leads und Personen. Die Tabellen sind wie folgt aufgebaut:

Table 1: people
- Name: Mustermann
- Vorname: Max
- Firma: IBM
- Telefon: 079 123 45 43
- Email: max.mustermann@ibm.ch
- Position: Entwicklungsleiter
- Abteilung: F&E
- HatFirmaVerlassen: Ja

Table 2: organizations
- Name: IBM
- Adresse: Wesstrasse 3, 8000 Zürich, Schweiz
- DistanzZH: 5
- DistanzChur: 90
- Groesse: 5000 Mitarbeiter
- UmsatzInMio: 5Mio CHF
- Klassifizierung_Cudos_Trail: ["0 - abklären"|"1 - Kunde"|"2 - ex Kunde"|"3 - Potentieller Kunde"|"4 - Kein Interesse"|"5 - Keine SW/Kein Potential"|"6 - interessiert - zu weit entfernt"]
- Klassifizierung_Pruefsyseme: ["0 - abklären"|"1 - High Potential"|"2 - Regelmässig Nachfassen"|"3 - Wenig Potential"|"5 - Kein Potential"]
- Klassifizierung_AI: ["0 - abklären"|"1 - High Potential"|"2 - Regelmässig Nachfassen"|"3 - Wenig Potential"|"5 - Kein Potential"]
- Klassifizierung_Software:["0 - abklären"|"1 - High Potential"|"2 - Regelmässig Nachfassen"|"3 - Wenig Potential"|"5 - Kein Potential"]
- Webseite: www.ibm.ch
Suche bei den Klassifizierungen immer mit LIKE %0%, %1%, %2%, %3% etc.

Table 3: leads
- Name: Projekt 1
- Firma: IBM
- Art: AI
- Verantwortlich: Max Mustermann
- Gewichteter_Betrag: 10000 CHF
- Einsatzdauer: 6 Monate
- Startdatum: 01.01.2023
- Status: [inaktiv|gewonnen|verloren|gestorben]

Die Spalte Firma in den Tabellen leads und people ist ein Schlüssel für organizations->Name.

Die Anzahl der Ergebnisse muss auf 50 Zeilen begrenzt werden, wählen Sie nur die für Ihre Abfrage erforderlichen Felder aus.
Wenn es mehr als 50 Zeilen gibt, sollte die Abfrage eine zusätzliche Informationsmeldung zurückgeben.
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

    def handle_tool_call(self, tool_call, messages, request_id = None):
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


