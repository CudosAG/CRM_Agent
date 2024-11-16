import os
import requests
import sys
import json
from dotenv import load_dotenv
load_dotenv()

sys.path.append('common')
from common.gpt import get_single_completion # type: ignore

BASE_URL = 'http://localhost:6000/crm'
# BASE_URL = 'https://baettig.org/crm'
SQL_URL = BASE_URL+'/sqlquery'
PLAIN_URL = BASE_URL+'/query'
TODO_URL = BASE_URL+'/todos'

RETOS_API_TOKEN = os.environ.get('RETOS_API_TOKEN')
if RETOS_API_TOKEN is None:
    raise ValueError('RETOS_API_TOKEN nicht in Umgebungsvariablen gefunden')

tests_todo = [ 

        { "question":"Welche todos gibt es?",
            "test":"Enthält die Antwort eine Liste von todos? Antworte NUR mit 'JA' oder 'NEIN'."
        },
        { "question":"Füge ein todo hinzu: Name: Max1, Firma: IBM1, Notiz: Test, Deadline: 2023-12-31",
            "test":"War die Aktion erfolgreich? Antworte NUR mit 'JA' oder 'NEIN'."
        },
        { "question":"Füge ein todo hinzu: Name: Max2, Firma: IBM2, Notiz: Test, Deadline: 2023-12-31",
            "test":"War die Aktion erfolgreich? Antworte NUR mit 'JA' oder 'NEIN'."
        },
         { "question":"Welche todos gibt es?",
            "test":"Enthält die Antwort eine Liste von todos? Antworte NUR mit 'JA' oder 'NEIN'."
        },
        { "question":"Lösche das Todo 1",
            "test":"War die Aktion erfolgreich? Antworte NUR mit 'JA' oder 'NEIN'."
        },
         { "question":"Welche todos gibt es?",
            "test":"Enthält die Antwort eine Liste von todos? Antworte NUR mit 'JA' oder 'NEIN'."
        }
          
]

tests_crm = [ 
        { "question":"wieviele einträge hat es in der tabelle organizations?",
          "test":"Enthält die Antwort eine Aussage über die Anzahl Einträge, die >0 ist? Antworte NUR mit 'JA' oder 'NEIN'."
        },
          
        { "question":"Welche Firmen gibt es in Fahrweid",
          "test":"Enthält die Antwort CUDOS AG, Antworte NUR mit 'JA' oder 'NEIN'."
        },
          
        { "question":"Bei welchen Organisationen ist ein CTO erfasst? Gib mir auch NAme/Vorname zurück",
          "test":"Enthält die Antwort eine Liste von Organisationen? Antworte NUR mit 'JA' oder 'NEIN'."
        },

        { "question":"Bei welchen Organisationen im Umkreis <10km um Zürich ist ein CTO erfasst? Gib mir auch NAme/Vorname zurück",
          "test":"Enthält die Antwort eine Liste von Organisationen? Antworte NUR mit 'JA' oder 'NEIN'."
        },        
        { "question":"Welche offenen potentiale mit startdatum < 31.12.24 gibt es?",
           "test":"Enthält die Antwort eine Liste von Potenitalen? Antworte NUR mit 'JA' oder 'NEIN'."
        },
        { "question":"Welche offenen potentiale gibt es mit startdatum < 31.12.24? Gib Name, Kunde, Startdatum und status zurück",
           "test":"Enthält die Antwort eine Liste von Potenitalen? Antworte NUR mit 'JA' oder 'NEIN'."
        },        
]
          
def test_ai(test):
    headers = {'Authorization': RETOS_API_TOKEN}
    
    try:
        response = requests.get(f"{PLAIN_URL}?query={test['question']}", headers=headers)
        response.raise_for_status()  # Wirft eine Ausnahme bei HTTP-Fehlern
        response_data = response.json()
        print(response_data)
        
        ans = get_single_completion(test["test"] + "\nAntwort: " + json.dumps(response_data))
        
        return ans
    except requests.exceptions.RequestException as e:
        print("Fehler bei der API-Anfrage:", e)
        return None  
    except json.JSONDecodeError:
        print("Fehler beim Dekodieren der JSON-Antwort.")
        return None  
    
def test_todo(test):
    headers = {'Authorization': RETOS_API_TOKEN}
    
    try:
        response = requests.get(f"{TODO_URL}?query={test['question']}", headers=headers)
        response.raise_for_status()  # Wirft eine Ausnahme bei HTTP-Fehlern
        response_data = response.json()
        print(response_data)
        
        ans = get_single_completion(test["test"] + "\nAntwort: " + json.dumps(response_data))
        
        return ans
    except requests.exceptions.RequestException as e:
        print("Fehler bei der API-Anfrage:", e)
        return None  
    except json.JSONDecodeError:
        print("Fehler beim Dekodieren der JSON-Antwort.")
        return None  
    
if __name__ == '__main__':
    tests_made = 0
    tests_passed = 0

    def update_stats(ans):
        global tests_made
        global tests_passed
        tests_made += 1
        if ans == "JA":
            tests_passed += 1
        print(f"Tests passed: {tests_passed}/{tests_made}")

    for test in tests_crm:
         print(test["question"])
         ans = test_ai(test)
         update_stats(ans)
         print(ans)
    for test in tests_todo:
        print(test["question"])
        ans = test_todo(test)
        update_stats(ans)
        print(ans)