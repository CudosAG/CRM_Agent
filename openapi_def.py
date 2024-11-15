OPENAPI_DEF = """
    {
  "openapi": "3.1.0",
  "info": {
    "title": "Get CRM Information",
    "description": "Provides access to Companies, People and Leads in the CRM system.",
    "version": "v1.0.0"
  },
  "servers": [
    {
      "url": "https://baettig.org"
    }
  ],
  "paths": {
    "/crm/query": {
      "get": {
        "description": "Ask questions about the CRM data",
        "operationId": "Query",
    
        "parameters": [
          {
            "name": "query",
            "in": "query",
            "description": "Talk to an agent who can answer questions about the data. The agent understands natural language and has access to a database. There are three tables in the database: 'organizations', 'people' and 'leads'. The organizations table has the following fields: Organisationsname,Webseite,\\"Umsatz (MIO CHF)\\",\\"Distanz ZH (km)\\",zuständig,\\"Distanz Chur (km)\\",\\"primäre E-Mail\\",Branche,Rechnungsadresse,\\"Rechnung PLZ\\",\\"Rechnung Postfach\\",\\"Rechnung Ort\\",\\"Rechnung Land\\",\\"Klassifizierung Softwareentwicklung und -testing \\",\\"Klassifizierung Prüfsysteme\\",\\"Klassifizierung AI (Künstliche Intelligenz)\\",\\"Klassifizierung Azure\\",\\"Klassifizierung Traineeprogramm\\",\\"Klassifizierung swissICT Booster 50+\\",Typ,Beschreibung,Unternehmenszweck,Verwaltungsrat,Zeichnungsberechtigte,Kundenart The leads table has the following fields: Potentialname,\\"Potential Nr.\\",Organisationsname,Art,Personename,zuständig,Verkaufskanal,erstellt,Kampagne,geändert,\\"aus Lead erstellt\\",BU,Projektnummer,\\"Betrag Engineering\\",Wahrscheinlichkeit,\\"Betrag Material\\",\\"Gewichteter Betrag Engineering\\",\\"Einsatzdauer (Mt.)\\",\\"Betrag Externe\\",Identifiziert,Offeriert,Geschlossen,\\"Grund Verloren\\",\\"Potential Abschluss\\",Endstatus,\\"Voraussichtliches Startdatum\\" The people table has the following fields: Anrede,Vorname,Nachname,\\"Personen Nr.\\",Organisation,\\"Akad. Titel\\",\\"Telefon Büro\\",Position,\\"mobiles Telefon\\",\\"Job Level\\",\\"Department / Business Unit\\",\\"primäre E-Mail\\",zuständig,erstellt,\\"Hat Unternehmen verlassen\\",\\"aus Lead erstellt\\",\\"Info Unternehmen verlassen\\",geändert,Straße,PLZ,Postfach,Ort,Land,Beschreibung,\\"Letter Language\\",Newsletter/E-Mail,\\"Typ Zusammenarbeit\\",\\"Grund Newsletter/E-Mail Nein\\",\\"Trainee-Programm vorgestellt\\",\\"HR Bulletin\\",Kontakthistorie,\\"Blog abonniert?\\",Weihnachtsgeschenke,Trainee-Newsletter,Überbringer,Task/Kampagne,Task-Status,\\"*Grund für Absage\\",\\"Wiedervorlage Datum\\",\\"Fall geschlossen\\"",
            "required": true,
            "schema": {
              "type": "string"
            }
          }
        ],
        
        "deprecated": false
      }
    }
  },
  "components": {
    "schemas": {}
  }
}"""