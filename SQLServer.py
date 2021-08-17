from sqlalchemy import engine

class Server():

    # Represents a Microsoft SQL Server instance pointing to a database in it.

    def __init__(self, ServerName, DatabaseName):
        self.ServerName = ServerName
        self.DatabaseName = DatabaseName

    def connect(self):
        try:
            Engine = engine.create_engine(f'mssql+pyodbc://{self.ServerName}/{self.DatabaseName}?driver=SQL+Server+Native+Client+11.0')
            self.Connection = Engine.connect()
            return True
        except:
            return False

    def run_command(self, Command):
        try:
            self.Connection.execute(Command)
            return True
        except:
            return False
