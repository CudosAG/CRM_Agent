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
    "/crm/sqlquery": {
      "get": {
        "description": "Get timesheet data",
        "operationId": "SQLQuery",
    
        "parameters": [
          {
            "name": "query",
            "in": "query",
            "description": "Query the crm database'.
There are three tables in the database: 'organizations', 'people' and 'leads'.
The organizations table has the following fields:
Organisationsname,Webseite,"Umsatz (MIO CHF)","Distanz ZH (km)",zuständig,"Distanz Chur (km)","primäre E-Mail",Branche,Rechnungsadresse,"Rechnung PLZ","Rechnung Postfach","Rechnung Ort","Rechnung Land","Klassifizierung Softwareentwicklung und -testing ","Klassifizierung Prüfsysteme","Klassifizierung AI (Künstliche Intelligenz)","Klassifizierung Azure","Klassifizierung Traineeprogramm","Klassifizierung swissICT Booster 50+",Typ,Beschreibung,Unternehmenszweck,Verwaltungsrat,Zeichnungsberechtigte,Kundenart",
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