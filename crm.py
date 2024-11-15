import pandas as pd
from pandasql import sqldf
import json

class Crm():
    __instance = None
    organiziations = None

    def __load_organization_data(self):
        print("Loading Organization data...")
        self.organizations = pd.read_csv("data/Organisationen.csv")
        print("...Organization data successfully loaded")
        
    def __load_data(self):
        print("Loading data...")
        self.__load_organization_data()
        print("...data successfully loaded")
        
    def get_data(self, sql_query):
        try:
            if sql_query is None:
                raise ValueError("No SQL query provided")
            
            print("Executing query: ", sql_query)
            result = sqldf(sql_query, self.__dict__)
        except Exception as e:
            return json.dumps({"error": str(e)})
        
        result = result.to_json(orient="records")
        return result
       
    def __new__(self):
        if not self.__instance:
            print('Creating new instance')
            self.__instance = super(Crm, self).__new__(self)
            self.__instance.__load_data()
        
        return self.__instance