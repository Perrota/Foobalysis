#! C:\Users\Marcelo\Documents\Documentos\Portfolio\Access\Musica2\env37\Scripts\python.exe

from PyQt5 import QtCore, QtGui, QtWidgets
from SQLServer import Server
from FoobarDatabase import Database
import os
import json

class Ui_EntryWindow(QtWidgets.QDialog):
    
    CurrentPath_String = os.path.dirname(os.path.dirname(__file__))
    ConfigFile_String = os.path.join(CurrentPath_String, 'Config.json')
    LoadData_pyqtSignal = QtCore.pyqtSignal()

    def setupUi(self, EntryWindow):

        self.EntryWindow = EntryWindow
        self.EntryWindow.setObjectName("EntryWindow")
        self.EntryWindow.resize(225, 115)
        self.EntryWindow.setWindowTitle("Login")
        self.EntryWindow.setWindowIcon(QtGui.QIcon(os.path.join(self.CurrentPath_String, 'fobalisis.ico')))

        Server_QLabel = QtWidgets.QLabel(self.EntryWindow)
        Server_QLabel.setGeometry(QtCore.QRect(20, 20, 50, 20))
        Server_QLabel.setObjectName("Server_QLabel")
        Server_QLabel.setText("Server:")

        DatabaseLabel_QLabel = QtWidgets.QLabel(self.EntryWindow)
        DatabaseLabel_QLabel.setGeometry(QtCore.QRect(20, 50, 50, 20))
        DatabaseLabel_QLabel.setObjectName("DatabaseLabel_QLabel")
        DatabaseLabel_QLabel.setText("Database:")

        self.ServerTextBox_QLineEdit = QtWidgets.QLineEdit(self.EntryWindow)
        self.ServerTextBox_QLineEdit.setGeometry(QtCore.QRect(80, 20, 128, 20))
        self.ServerTextBox_QLineEdit.setObjectName("ServerTextBox_QLineEdit")

        self.DatabaseTextBox_QLineEdit = QtWidgets.QLineEdit(self.EntryWindow)
        self.DatabaseTextBox_QLineEdit.setGeometry(QtCore.QRect(80, 50, 128, 20))
        self.DatabaseTextBox_QLineEdit.setObjectName("DatabaseTextBox_QLineEdit")

        self.OpenButton_QPushButton = QtWidgets.QPushButton(self.EntryWindow)
        self.OpenButton_QPushButton.setGeometry(QtCore.QRect(130, 80, 75, 23))
        self.OpenButton_QPushButton.setObjectName("OpenButton_QPushButton")
        self.OpenButton_QPushButton.setText("Open")
        self.OpenButton_QPushButton.clicked.connect(self.OpenButton_QPushButton_onButtonClicked)

        Help_QPushButton = QtWidgets.QPushButton(self.EntryWindow)
        Help_QPushButton.setGeometry(QtCore.QRect(25, 80, 75, 23))
        Help_QPushButton.setObjectName('Help_QPushButton')
        Help_QPushButton.setText('Help')
        Help_QPushButton.setFlat(True)
        Help_QPushButton.clicked.connect(self.Help_QPushButton_onButtonClicked)

        self.load_saved_data()

        QtCore.QMetaObject.connectSlotsByName(self.EntryWindow)

    def load_saved_data(self):
        if os.path.isfile(self.ConfigFile_String):
            with open(self.ConfigFile_String, "r") as File:
                Configs_Dictionary = json.load(File)
            self.ServerTextBox_QLineEdit.setText(Configs_Dictionary['Server'])
            self.DatabaseTextBox_QLineEdit.setText(Configs_Dictionary['Database'])
            self.OpenButton_QPushButton.setFocus()

    def Help_QPushButton_onButtonClicked(self):
        QMessageBox = QtWidgets.QMessageBox()
        QMessageBox.setText("Welcome! This app connects to an instance of Microsoft SQL Server in order to save your data. Please enter the name of the server and database you've chosen for this application. If this is your first time setting up the application, enter the name of an existing database that you want to use to host your data.")
        QMessageBox.setIcon(QtWidgets.QMessageBox.Question)
        QMessageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        QMessageBox.setWindowTitle('Help')
        QMessageBox.setWindowIcon(QtGui.QIcon(os.path.join(self.CurrentPath_String, 'fobalisis.ico')))
        QMessageBox.show()
        QMessageBox.exec_()

    def OpenButton_QPushButton_onButtonClicked(self):

        self.Server_String = self.ServerTextBox_QLineEdit.text()
        self.Database_String = self.DatabaseTextBox_QLineEdit.text()

        if self.Server_String != "" and self.Database_String != "":
            self.attempt_connection()
        else:
            self.display_error_message('Please fill both fields.')

    def attempt_connection(self):
    
        self.Server = Server(self.Server_String, self.Database_String)
        # try:
        self.Server.connect()
        self.Database = Database(self.Server)
        HasCorrectStructure_Boolean = self.Database.check_structure()
        if HasCorrectStructure_Boolean:
            self.open_main()
        else:
            self.display_repair_message()
        # except:
        #     self.display_error_message("Couldn't connect to SQL Server.")

    def display_error_message(self, ErrorMessage):
        QMessageBox = QtWidgets.QMessageBox()
        QMessageBox.setText(ErrorMessage)
        QMessageBox.setIcon(QtWidgets.QMessageBox.Critical)
        QMessageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        QMessageBox.setWindowTitle('Error')
        QMessageBox.setWindowIcon(QtGui.QIcon(os.path.join(self.CurrentPath_String, 'fobalisis.ico')))
        QMessageBox.exec_()

    def display_repair_message(self):

        def repair_database(i):
            if i.text() == "&Yes":
                
                ScriptsFolder_String = os.path.join(os.path.dirname(__file__), 'SQL Scripts')
                FileNames_List = os.listdir(ScriptsFolder_String)
                FilePaths_List = [os.path.join(ScriptsFolder_String, FileName) for FileName in FileNames_List]

                self.MusicConn.repair_database(FilePaths_List)
                self.display_success_message()

        QMessageBox = QtWidgets.QMessageBox()
        QMessageBox.setText("There's an error with the database, as not every table necessary was identified. Do you want to recreate them from scratch?")
        QMessageBox.setIcon(QtWidgets.QMessageBox.Question)
        QMessageBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        QMessageBox.setWindowTitle("Incomplete database")
        QMessageBox.buttonClicked.connect(repair_database)
        QMessageBox.setWindowIcon(QtGui.QIcon(os.path.join(self.CurrentPath_String, 'fobalisis.ico')))
        QMessageBox.exec_()

    def display_success_message(self):

        def continue_(i):
            self.open_main()

        QMessageBox = QtWidgets.QMessageBox()
        QMessageBox.setText = "Done."
        QMessageBox.setIcon(QtWidgets.QMessageBox.Information)
        QMessageBox.setWindowTitle("Success")
        QMessageBox.buttonClicked.connect(continue_)
        QMessageBox.setWindowIcon(QtGui.QIcon(os.path.join(self.CurrentPath_String, 'fobalisis.ico')))
        QMessageBox.exec_()

    def open_main(self):

        def save_config():
            Configs_Dictionary = dict({'Server': self.ServerTextBox_QLineEdit.text(), 'Database': self.DatabaseTextBox_QLineEdit.text()})
            with open(self.ConfigFile_String, 'w') as File:
                json.dump(Configs_Dictionary, File)

        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        save_config()
        self.LoadData_pyqtSignal.emit()
        QtWidgets.QApplication.restoreOverrideCursor()
        self.EntryWindow.close()
