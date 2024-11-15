
import sys
from dotenv import load_dotenv
load_dotenv()

sys.path.append('common')
from common.gpt import get_single_completion # type: ignore

PROMPT = '''
Bereinige den Prompt, damit er sich im nächsten schritt besser eignet für eine Anfrage an die API.
Berücksichtige folgende Regeln:
- Wenn der User nach Ort fragt, ersetze "Ort" durch "Rechnung Ort"
- Wenn der User nach Dem name einer Firma fragt, ersetze "Name" durch "Organisationsname"
- Wenn der User nach Distanz fragt, ersetze "Distanz" durch "Distanz ZH"
'''

def preprocess(prompt):
    ans = get_single_completion(PROMPT+"\n---\n"+prompt)
    return ans