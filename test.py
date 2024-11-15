import os
import requests
import sys
import json
from dotenv import load_dotenv
load_dotenv()

sys.path.append('common')
from common.gpt import get_single_completion # type: ignore

#BASE_URL = 'http://localhost:6000/crm'
BASE_URL = 'https://baettig.org/crm'
SQL_URL = BASE_URL+'/sqlquery'
PLAIN_URL = BASE_URL+'/query'

RETOS_API_TOKEN = os.environ.get('RETOS_API_TOKEN')
if RETOS_API_TOKEN is None:
    raise ValueError('RETOS_API_TOKEN nicht in Umgebungsvariablen gefunden')

def test_ai(query):
        headers = {'Authorization': RETOS_API_TOKEN}
            
        # Hier solltest du sicherstellen, dass der Service tatsächlich läuft und die erwartete Antwort zurückgibt
        response = requests.get(f"{PLAIN_URL}?query={query}", headers=headers)
        response_data = response.json()
        ans = get_single_completion("Enthält das folgende Objekt eine Aussage über eine Anzahl von Einträgen? Bitte Antwote NUR mit 'JA' oder 'NEIN': "+
                json.dumps(response_data))
        return ans

if __name__ == '__main__':
    query = "wieviele einträge hat es in der tabelle organizations? Gib mir die Antwort als JSON-Objekt."
    ans = test_ai(query)
    print(ans)