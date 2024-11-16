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
MONEYHOUSE_URL = BASE_URL+'/moneyhouse'

RETOS_API_TOKEN = os.environ.get('RETOS_API_TOKEN')
if RETOS_API_TOKEN is None:
    raise ValueError('RETOS_API_TOKEN nicht in Umgebungsvariablen gefunden')

tests = [ 
        { 
            "question":"Ist Google in der Schweiz noch aktiv",
            "test":"Enthält die Antwort informationen darüber, ob Google aktiv ist? Antworte NUR mit 'JA' oder 'NEIN'."
        }
          
]
          
def test_ai(test):
    headers = {'Authorization': RETOS_API_TOKEN}
    
    try:
        response = requests.get(f"{MONEYHOUSE_URL}?query={test['question']}", headers=headers)
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

    for test in tests:
        print(test["question"])
        ans = test_ai(test)
        update_stats(ans)
        print(ans)