
import sys
from dotenv import load_dotenv
load_dotenv()

sys.path.append('common')
from common.gpt import get_single_completion # type: ignore

PROMPT = '''
Bereinige den Prompt, damit er sich im nächsten schritt besser eignet für eine Anfrage an die API.
Du hast 3 Tabellen mit folgenden Feldern und Beispielwerten:

Table 1: people
- Name: Mustermann
- Vorname: Max
- Firma: IBM
- Telefon: 079 123 45 43
- Email: max.mustermann@ibm.ch
- Position: Entwicklungsleiter
- Abteilung: F&E
- HatFirmaVerlassen: Ja

Table 2: organization
- Name: IBM
- Adresse: Wesstrasse 3, 8000 Zürich, Schweiz
- DistanzZH: 5km
- DistanzChur: 90km
- Groesse: 5000 Mitarbeiter
- Umsatz: 5Mio CHF
- Klassifizierung_Cudos_Trail: [0 - abklären|1 - High Potential|2 - Regelmässig Nachfassen|3 - Wenig Potential|5 - Kein Potential]  
- Klassifizierung_Pruefsyseme: 1 - High Potential
- Klassifizierung_AI: 1 - High Potential
- Klassifizierung_Software: 3 - Wenig Potential

Table 3: leads
- Name: Projekt 1
- Firma: IBM
- Art: AI
- Verantwortlich: Max Mustermann
- Gewichteter_Betrag: 10000 CHF
- Einsatzdauer: 6 Monate
- Startdatum: 01.01.2023
- Status: [inaktiv|gewonnen|verloren|gestorben]
 
Formuliere die Anfrage so um, dass sie auf die oben genannte Struktur passt, wobei "Firma" in leads und people ein Schlüssel für organization->Name ist.
'''

def preprocess(prompt):
    ans = get_single_completion(PROMPT+"\n---\n"+prompt)
    return ans


if __name__ == '__main__':
    preprocess("Wie viele Firmen gibt es in Fahrweid")