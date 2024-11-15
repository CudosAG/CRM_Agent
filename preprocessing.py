
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

Table 2: organizations
- Name: IBM
- Adresse: Wesstrasse 3, 8000 Zürich, Schweiz
- DistanzZH: 5
- DistanzChur: 90
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
- Status: [inaktiv|Closed Won|Closed Lost|gestorben]
 
Formuliere die Anfrage so um, dass sie auf die oben genannte Struktur passt, wobei "Firma" in leads und people ein Schlüssel für organizations->Name ist.

Beispiel:

*Originaler Prompt:*
Bei welchen Organisationen ist ein CTO erfasst?

*Bereinigter Prompt:*

Aufgabe: Suche nach Organisationen, bei denen ein CTO in der Tabelle `people` erfasst ist und gib Name und Ort der Firma zurück. 
Dabei wird die `Firma` in der Tabelle `people` als Schlüssel für den `Name` in der Tabelle `organizations` verwendet.

Filterkriterien und Vorgehen:
- `Position` in `people` muss wie "%CTO%" sein.
- `Firma` in `people` ist ein Schlüssel für `organizations->Name`.
- Gebe den `Name` und die `Adresse` der Firma zurück, die den CTO erfasst hat.

---- 
HALTE DICH KURZ und PRÄZISE, GIB NUR DEN BEREINGTEN PROMPT mit Aufgabe, Filterkriterien und Vorgehen zurück.
'''

def preprocess(prompt):
    ans = get_single_completion(PROMPT+"\n---\n"+prompt)
    return ans


if __name__ == '__main__':
    fragen = [
        "Wie viele Firmen gibt es in Fahrweid", 
        "Welche Firmen gibt es in Fahrweid", 
        "Bei welchen Organisationen ist ein CTO erfasst?"
    ]
    for frage in fragen:
        print("Original: "+frage)
        print(preprocess(frage)+"\n")
    