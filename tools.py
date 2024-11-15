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
Die Tabelle organizations hat folgende Felder:
Organisationsname,Webseite,"Umsatz (MIO CHF)","Distanz ZH (km)",zuständig,"Distanz Chur (km)","primäre E-Mail",Branche,Rechnungsadresse,"Rechnung PLZ","Rechnung Postfach","Rechnung Ort","Rechnung Land","Klassifizierung Softwareentwicklung und -testing ","Klassifizierung Prüfsysteme","Klassifizierung AI (Künstliche Intelligenz)","Klassifizierung Azure","Klassifizierung Traineeprogramm","Klassifizierung swissICT Booster 50+",Typ,Beschreibung,Unternehmenszweck,Verwaltungsrat,Zeichnungsberechtigte,Kundenart"

Die Tabelle leads hat folgende Felder:
Potentialname,"Potential Nr.",Organisationsname,Art,Personename,zuständig,Verkaufskanal,erstellt,Kampagne,geändert,"aus Lead erstellt",BU,Projektnummer,"Betrag Engineering",Wahrscheinlichkeit,"Betrag Material","Gewichteter Betrag Engineering","Einsatzdauer (Mt.)","Betrag Externe",Identifiziert,Offeriert,Geschlossen,"Grund Verloren","Potential Abschluss",Endstatus,"Voraussichtliches Startdatum"

Der Tabelle people hat folgende Felder:
Anrede,Vorname,Nachname,"Personen Nr.",Organisation,"Akad. Titel","Telefon Büro",Position,"mobiles Telefon","Job Level","Department / Business Unit","primäre E-Mail",zuständig,erstellt,"Hat Unternehmen verlassen","aus Lead erstellt","Info Unternehmen verlassen",geändert,Straße,PLZ,Postfach,Ort,Land,Beschreibung,"Letter Language",Newsletter/E-Mail,"Typ Zusammenarbeit","Grund Newsletter/E-Mail Nein","Trainee-Programm vorgestellt","HR Bulletin",Kontakthistorie,"Blog abonniert?",Weihnachtsgeschenke,Trainee-Newsletter,Überbringer,Task/Kampagne,Task-Status,"*Grund für Absage","Wiedervorlage Datum","Fall geschlossen"

Die Tabellen organization und people sind über das Feld "Organisation" in der people Tabelle verknüpft. Das Feld "Organisation" enthält den Namen der Organisation mit dem Präfix "Accounts::::".

Potentiale können zu Organisationen zugeordnet werden, indem das Feld "Organisationsname" in der leads Tabelle mit dem Feld "Organisationsname" in der organizations Tabelle abgeglichen wird, wobei lead.Organisationsname wiederum das Präfix mit "Accounts::::" enthält.

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


