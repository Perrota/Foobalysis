from sqlalchemy import engine

class Server():

    # Represents a Microsoft SQL Server instance pointing to a database in it.

    def __init__(self, ServerName):
        self.ServerName = ServerName

    def connect_to(self, DatabaseName):
        return Database(self.ServerName, DatabaseName)

class Database():

    def __init__(self, ServerName, DatabaseName):
        self.Name = DatabaseName
        Engine = engine.create_engine(f'mssql+pyodbc://{ServerName}/{DatabaseName}?driver=SQL+Server+Native+Client+11.0')
        self.Connection = Engine.connect()

    def run_command(self, Command):
        try:
            self.Connection.execute(Command)
            return True
        except:
            return False
