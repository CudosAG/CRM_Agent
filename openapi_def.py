OPENAPI_DEF = """
{
   "openapi":"3.1.0",
   "info":{
      "title":"Get CRM Information",
      "description":"Provides access to Companies, People and Leads in the CRM system.",
      "version":"v1.0.0"
   },
   "servers":[
      {
         "url":"https://baettig.org"
      }
   ],
   "paths":{
      "/crm/query":{
         "get":{
            "description":"Ask questions about the CRM data",
            "operationId":"Query",
            "parameters":[
               {
                  "name":"query",
                  "in":"query",
                  "description":"Talk to an agent who can answer questions about the data. The agent understands natural language and has access to a database. There are three tables in the database: 'organizations', 'people' and 'leads'. 
The organizations table has informations about an organization like name, address, size, ...
the leads table has information about leads like name, organization, size, ...
the people table has information about people like firstname, lastname, organziation, email, phone, ...
Always limit the number of answers to 20 entries",
                  "required":true,
                  "schema":{
                     "type":"string"
                  }
               }
            ],
            "deprecated":false
         }
      },
      "/crm/todos":{
         "get":{
            "description":"Manage the todo list",
            "operationId":"Todos",
            "parameters":[
               {
                  "name":"query",
                  "in":"query",
                  "description":"Ask questions about the todo list like 'What todos are there?' or 'Add a todo: Name: Max1, Firma: IBM1, Notiz: Test, Deadline: 2023-12-31' or 'delete todo with UID 123'. Name is always the Name of the User",
                  "required":true,
                  "schema":{
                     "type":"string"
                  }
               }
            ],
            "deprecated":false
         }
      },
      "/crm/moneyhouse":{
         "get":{
            "description":"Get information on companies from an online company directory",
            "operationId":"Moneyhouse",
            "parameters":[
               {
                  "name":"query",
                  "in":"query",
                  "description":"Ask questions about companies from a company directory. Questions might be 'How many employees does Cudos have?' or 'Tell me if Cudos is still active.' There is information about the company age, revenue, number of employees and if the company is still active.",
                  "required":true,
                  "schema":{
                     "type":"string"
                  }
               }
            ],
            "deprecated":false
         }
      }
   },
   "components":{
      "schemas":{
         
      }
   }
}"""