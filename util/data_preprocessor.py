import argparse
import pandas as pd
import re

def process_organizations(folder_in, folder_out):
    organizations = pd.read_csv(folder_in + "/Organisationen.csv")
    
    organizations_transformed = organizations[[
        "Organisationsname",
        "Distanz ZH (km)",
        "Distanz Chur (km)",
        "Umsatz (MIO CHF)",
        "Mitarbeiter",
        "Klassifizierung Softwareentwicklung und -testing ",
        "Klassifizierung Prüfsysteme",
        "Klassifizierung AI (Künstliche Intelligenz)",
        "Klassifizierung Traineeprogramm",
        "Webseite",
        "zuständig",
        "Branche"
    ]]
    
    organizations_transformed = organizations_transformed.rename(columns={
        "Organisationsname": "Name",
        "Distanz ZH (km)": "DistanzZH",
        "Distanz Chur (km)": "DistanzChur",
        "Umsatz (MIO CHF)": "UmsatzInMio",
        "Klassifizierung Softwareentwicklung und -testing ": "Klassifizierung_Software",
        "Klassifizierung Prüfsysteme": "Klassifizierung_Pruefsysteme",
        "Klassifizierung AI (Künstliche Intelligenz)": "Klassifizierung_AI",
        "Klassifizierung Traineeprogramm": "Klassifizierung_Cudos_Trail",
        "Mitarbeiter": "Groesse",
        "zuständig": "Verantwortlich"
    })
    
    organizations_transformed['Adresse'] = organizations['Rechnungsadresse'] + ", " + organizations['Rechnung PLZ'] + " " + organizations['Rechnung Ort'] + ", " +  organizations['Rechnung Land']
    
    # klassifizierung_pattern = re.compile(r'(\d) - .*')
    # organizations_transformed['Klassifizierung_Software'] = organizations_transformed['Klassifizierung_Software'].str.replace(klassifizierung_pattern, r'\1', regex=True)
    # organizations_transformed['Klassifizierung_Pruefsysteme'] = organizations_transformed['Klassifizierung_Pruefsysteme'].str.replace(klassifizierung_pattern, r'\1', regex=True)
    # organizations_transformed['Klassifizierung_AI'] = organizations_transformed['Klassifizierung_AI'].str.replace(klassifizierung_pattern, r'\1', regex=True)
    # organizations_transformed['Klassifizierung_Cudos_Trail'] = organizations_transformed['Klassifizierung_Cudos_Trail'].str.replace(klassifizierung_pattern, r'\1', regex=True)
        
    organizations_transformed.to_csv(folder_out + "/Organisationen.csv", index=False)
    
def process_leads(folder_in, folder_out):
    leads = pd.read_csv(folder_in + "/Potentiale.csv")
    
    leads_transformed = leads[[
        "Potentialname",
        "Organisationsname",
        "Art",
        "zuständig",
        "Gewichteter Betrag Engineering",
        "Einsatzdauer (Mt.)",
        "Potential Abschluss",
        "Endstatus"
    ]]
    
    leads_transformed = leads_transformed.rename(columns={
        "Potentialname": "Name",
        "Organisationsname": "Firma",
        "Art": "Art",
        "zuständig": "Verantwortlich",
        "Gewichteter Betrag Engineering": "Gewichteter_Betrag",
        "Einsatzdauer (Mt.)": "Einsatzdauer",
        "Potential Abschluss": "Startdatum",
        "Endstatus": "Status"
    })
    
    leads_transformed['Firma'] = leads_transformed['Firma'].str.replace('Accounts::::', '')
    
    leads_transformed.to_csv(folder_out + "/Potentiale.csv", index=False)

def process_people(folder_in, folder_out):
    people = pd.read_csv(folder_in + "/Personen.csv")
    
    people_transformed = people[[
        "Vorname",
        "Nachname",
        "Organisation",
        "primäre E-Mail",
        "Position",
        "Department / Business Unit",
        "Hat Unternehmen verlassen",
        "Trainee-Programm vorgestellt"
    ]]
    
    people_transformed = people_transformed.rename(columns={
        "Telefon Büro": "Telefon",
        "primäre E-Mail": "Email",
        "Department / Business Unit": "Abteilung",
        "Organisation": "Firma",
        "Hat Unternehmen verlassen": "HatFirmaVerlassen",
        "Nachname": "Name",
        "Trainee-Programm vorgestellt": "CudosTrailVorgestellt"
    })
    
    people_transformed['Telefon'] = people['Telefon Büro'] + " / " + people['mobiles Telefon']
    
    people_transformed['Firma'] = people_transformed['Firma'].str.replace('Accounts::::', '')
    
    people_transformed.to_csv(folder_out + "/Personen.csv", index=False)

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Process files from input folder to output folder")
    parser.add_argument("-i", "--input", required=True, help="Input folder path")
    parser.add_argument("-o", "--output", required=True, help="Output folder path")
    args = parser.parse_args()

    folder_in = args.input
    folder_out = args.output

    process_organizations(folder_in, folder_out)
    
    process_leads(folder_in, folder_out)
    
    process_people(folder_in, folder_out)

if __name__ == "__main__":
    main()