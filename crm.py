import pandas as pd
from pandasql import sqldf
import logging
import json

MAX_ANSWER_LENGTH = 20000

class Crm():
    __instance = None
    organiziations = None
    leads = None
    people = None

    def __load_organization_data(self):
        print("Loading Organization data...")
        self.organizations = pd.read_csv("data/Organisationen.csv")
        print("...Organization data successfully loaded")
        
    def __load_lead_data(self):
        print("Loading Lead data...")
        self.leads = pd.read_csv("data/Potentiale.csv")
        print("...Lead data successfully loaded")
        
    def __load_people_data(self):
        print("Loading People data...")
        self.people = pd.read_csv("data/Personen.csv")
        print("...People data successfully loaded")
        
    def __load_data(self):
        print("Loading data...")
        self.__load_organization_data()
        self.__load_lead_data()
        self.__load_people_data()
        print("...data successfully loaded")
        
    def get_data(self, sql_query):
        try:
            if sql_query is None:
                raise ValueError("No SQL query provided")
            
            print("Executing query: "+sql_query)
            result = sqldf(sql_query, self.__dict__)
        except Exception as e:
            print("Error in get_data: "+str(e))
            return json.dumps({"error": str(e)})
        
        result = result.to_markdown(index=False)
        if len(result) > MAX_ANSWER_LENGTH:
            print("Maximale Länge überschritten")
            result = result[:MAX_ANSWER_LENGTH]
            result = result + "\n... (truncated)"
        
        print("Query result: "+result)

        return result
       
    def __new__(self):
        if not self.__instance:
            print('Creating new instance')
            self.__instance = super(Crm, self).__new__(self)
            self.__instance.__load_data()
        
        return self.__instance