
import sys
from dotenv import load_dotenv
load_dotenv()

sys.path.append('common')
from common.gpt import get_single_completion # type: ignore

PROMPT = '''
Bereinige den Prompt, damit er sich im nächsten schritt besser eignet für eine Anfrage an die API.
Berücksichtige folgende Regeln:
- Die Adresse setzt sich aus mehreren Spalten zusammen: "Rechnung Ort" für die Ortschaft, "Rechnung PLZ" für die Postleitzahl und "Rechnungsadresse" für die Strasse. Versuche Fragen nach Orten entsprechend anzupassen indem du auf die entsprechenden Spalten Eigenschaften verweist.
- Wenn der User nach Dem name einer Firma fragt, ersetze "Name" durch "Organisationsname"
- Wenn der User nach Distanz fragt, ersetze "Distanz" durch "Distanz ZH"
'''

def preprocess(prompt):
    ans = get_single_completion(PROMPT+"\n---\n"+prompt)
    return ans