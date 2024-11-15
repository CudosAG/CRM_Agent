OPENAPI_DEF_CRM = """
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
      }
   },
   "components":{
      "schemas":{
         
      }
   }
}"""

OPENAPI_DEF_TODO = """
{
   "openapi":"3.1.0",
   "info":{
      "title":"Manage Todo List",
      "description":"Provides access to a todo list with ",
      "version":"v1.0.0"
   },
   "servers":[
      {
         "url":"https://baettig.org"
      }
   ],
   "paths":{
      "/crm/todos":{
         "get":{
            "description":"Manage the todo list",
            "operationId":"Query",
            "parameters":[
               {
                  "name":"query",
                  "in":"query",
                  "description":"Ask questions about the todo list like 'What todos are there?' or 'Add a todo: Name: Max1, Firma: IBM1, Notiz: Test, Deadline: 2023-12-31' or 'delete todo with UID 123'",
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