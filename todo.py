import pandas as pd
import pandasql as psql

class Todo:
    def __init__(self, filename='todos.csv'):
        self.filename = filename
        self.todos = self.load_todos()

    def load_todos(self):
        try:
            todos = pd.read_csv(self.filename)
        except FileNotFoundError:
            # Wenn die Datei nicht existiert, erstelle ein leeres DataFrame
            todos = pd.DataFrame(columns=['Name', 'Firma', 'Notiz', 'Deadline'])
        return todos

    def save_todos(self):
        self.todos.to_csv(self.filename, index=False)

    def add_todo(self, name, firma, notiz, deadline):
        new_todo = pd.DataFrame({'Name': [name], 'Firma': [firma], 'Notiz': [notiz], 'Deadline': [deadline]})
        self.todos = pd.concat([self.todos, new_todo], ignore_index=True)
        self.save_todos()

    def edit_todo(self, index, name=None, firma=None, notiz=None, deadline=None):
        if name is not None:
            self.todos.at[index, 'Name'] = name
        if firma is not None:
            self.todos.at[index, 'Firma'] = firma
        if notiz is not None:
            self.todos.at[index, 'Notiz'] = notiz
        if deadline is not None:
            self.todos.at[index, 'Deadline'] = deadline
        self.save_todos()

    def delete_todo(self, index):
        self.todos = self.todos.drop(index).reset_index(drop=True)
        self.save_todos()

    def query_todos(self, query):
        return psql.sqldf(query, locals())

    def display_todos(self):
        print("\nAktuelle To-Do-Liste:")
        print(self.todos)

def main():
    todo_list = Todo()

    while True:
        todo_list.display_todos()
        
        print("\nWähle eine Option:")
        print("1. To-Do hinzufügen")
        print("2. To-Do bearbeiten")
        print("3. To-Do löschen")
        print("4. To-Do abfragen (SQL)")
        print("5. Beenden")
        
        choice = input("Gib deine Wahl ein: ")

        if choice == '1':
            name = input("Name: ")
            firma = input("Firma: ")
            notiz = input("Notiz: ")
            deadline = input("Deadline: ")
            todo_list.add_todo(name, firma, notiz, deadline)

        elif choice == '2':
            index = int(input("Index des To-Dos, das du bearbeiten möchtest: "))
            name = input("Neuer Name (oder Enter überspringen): ")
            firma = input("Neue Firma (oder Enter überspringen): ")
            notiz = input("Neue Notiz (oder Enter überspringen): ")
            deadline = input("Neue Deadline (oder Enter überspringen): ")
            todo_list.edit_todo(index, name if name else None, firma if firma else None, notiz if notiz else None, deadline if deadline else None)

        elif choice == '3':
            index = int(input("Index des To-Dos, das du löschen möchtest: "))
            todo_list.delete_todo(index)

        elif choice == '4':
            sql_query = input("Gib deine SQL-Abfrage ein (z.B. SELECT * FROM todos WHERE Firma='XYZ'): ")
            result = todo_list.query_todos(sql_query)
            print("Abfrageergebnis:")
            print(result)

        elif choice == '5':
            break

        else:
            print("Ungültige Wahl. Bitte versuche es erneut.")

if __name__ == "__main__":
    main()
