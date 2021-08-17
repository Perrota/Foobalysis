from PyQt5 import QtCore, QtGui, QtWidgets
from os import path
import pandas as pd
from PandasModel import Model
import json

class Ui_viewsDialog(QtWidgets.QDialog):

    SQLstatement = QtCore.pyqtSignal()

    def setupUi(self, viewsDialog, dbConn, ThisFilePath):

        self.dbConn = dbConn
        self.ThisFilePath_String = ThisFilePath

        # Dialog window
        viewsDialog.setObjectName("viewsDialog")
        viewsDialog.setFixedSize(615, 384)
        viewsDialog.setWindowTitle("Custom Views")
        viewsDialog.setWindowIcon(QtGui.QIcon(path.join(self.ThisFilePath_String, 'fobalisis.ico')))
        
        # Label views
        Views_QLabel = QtWidgets.QLabel(viewsDialog)
        Views_QLabel.setGeometry(QtCore.QRect(130, 10, 30, 13))
        Views_QLabel.setObjectName("Views_QLabel")
        Views_QLabel.setText("Views")

        # List of views
        self.QListView = QtWidgets.QListView(viewsDialog)
        self.QListView.setGeometry(QtCore.QRect(20, 30, 256, 311))
        self.QListView.setObjectName("QListView")
        with open(path.join(self.ThisFilePath_String, 'Views.txt'), 'r') as File:
            JSON_Dictionary = json.load(File)
        self.Views_Dataframe = pd.DataFrame.from_dict(JSON_Dictionary, orient='index', columns=['Definition'])
        self.Views_Dataframe.reset_index(inplace=True)
        self.View_Model = Model(self.Views_Dataframe)
        self.QListView.setModel(self.View_Model)
        
        # Lable title
        Title_QLabel = QtWidgets.QLabel(viewsDialog)
        Title_QLabel.setGeometry(QtCore.QRect(290, 10, 31, 16))
        Title_QLabel.setObjectName("Title_QLabel")
        Title_QLabel.setText("Title:")

        # Title dialog box
        self.Title_QLineEdit = QtWidgets.QLineEdit(viewsDialog)
        self.Title_QLineEdit.setGeometry(QtCore.QRect(290, 30, 311, 20))
        self.Title_QLineEdit.setObjectName("Title_QLineEdit")

        # Label definition
        Definition_QLabel = QtWidgets.QLabel(viewsDialog)
        Definition_QLabel.setGeometry(QtCore.QRect(290, 60, 61, 16))
        Definition_QLabel.setObjectName("Definition_QLabel")
        Definition_QLabel.setText("Definition:")

        # Text Definition
        self.Definition_QPlainTextEdit = QtWidgets.QPlainTextEdit(viewsDialog)
        self.Definition_QPlainTextEdit.setGeometry(QtCore.QRect(290, 80, 311, 261))
        self.Definition_QPlainTextEdit.setObjectName("Definition_QPlainTextEdit")

        # Buttons
        self.Remove_QPushButton = QtWidgets.QPushButton(viewsDialog)
        self.Remove_QPushButton.setObjectName("Remove_QPushButton")
        self.Remove_QPushButton.setGeometry(QtCore.QRect(25, 350, 75, 23))
        self.Remove_QPushButton.setText("Remove")
        self.Remove_QPushButton.clicked.connect(self.Remove_QPushButton_onButtonClick)
        self.Load_QPushButton = QtWidgets.QPushButton(viewsDialog)
        self.Load_QPushButton.setGeometry(QtCore.QRect(195, 350, 75, 23))
        self.Load_QPushButton.setObjectName("Load_QPushButton")
        self.Load_QPushButton.setText("Load")
        self.Load_QPushButton.clicked.connect(self.Load_QPushButton_onButtonClick)
        self.Save_QPushButton = QtWidgets.QPushButton(viewsDialog)
        self.Save_QPushButton.setGeometry(QtCore.QRect(360, 350, 75, 23))
        self.Save_QPushButton.setObjectName("Save_QPushButton")
        self.Save_QPushButton.setText("Save")
        self.Save_QPushButton.clicked.connect(self.Save_QPushButton_onButtonClick)
        self.Apply_QPushButton = QtWidgets.QPushButton(viewsDialog)
        self.Apply_QPushButton.setGeometry(QtCore.QRect(440, 350, 75, 23))
        self.Apply_QPushButton.setObjectName("Apply_QPushButton")
        self.Apply_QPushButton.setText("Apply")
        self.Apply_QPushButton.clicked.connect(self.Apply_QPushButton_onButtonClick)
        self.Close_QPushButton = QtWidgets.QPushButton(viewsDialog)
        self.Close_QPushButton.setGeometry(QtCore.QRect(520, 350, 75, 23))
        self.Close_QPushButton.setObjectName("Close_QPushButton")
        self.Close_QPushButton.setText("Close")
        self.Close_QPushButton.clicked.connect(viewsDialog.close)

        QtCore.QMetaObject.connectSlotsByName(viewsDialog)

    def Remove_QPushButton_onButtonClick(self):

        SelectedElement_String = self.QListView.model().index(self.QListView.currentIndex().row(), 0).data()
        JSONFilePath_String = path.join(self.ThisFilePath_String, 'Views.txt')

        with open(JSONFilePath_String, 'r') as File:
            JSON_Dictionary = json.load(File)

        del JSON_Dictionary[SelectedElement_String]

        with open(JSONFilePath_String, 'w') as File:
            json.dump(JSON_Dictionary, File)

        self.Views_Dataframe = pd.DataFrame.from_dict(JSON_Dictionary, orient='index', columns=['Definition'])
        self.Views_Dataframe.reset_index(inplace=True)
        View_Model = Model(self.Views_Dataframe)
        self.QListView.setModel(View_Model)

    def Load_QPushButton_onButtonClick(self):
        ViewName_String = self.QListView.model().index(self.QListView.currentIndex().row(), 0).data()
        self.Title_QLineEdit.setText(ViewName_String)

        with open(path.join(self.ThisFilePath_String, 'Views.txt'), 'r') as File:
            JSON_Dictionary = json.load(File)
            self.Definition_QPlainTextEdit.setPlainText(JSON_Dictionary[ViewName_String])

    def Apply_QPushButton_onButtonClick(self):
        self.df = pd.read_sql_query(self.Definition_QPlainTextEdit.toPlainText(), self.dbConn.Connection)
        self.SQLstatement.emit()
    
    def Save_QPushButton_onButtonClick(self):
        
        strJSONFile = path.join(self.ThisFilePath_String, 'Views.txt')

        with open(strJSONFile, 'r') as File:
            JSON_Dictionary = json.load(File)
        
        JSON_Dictionary[self.Title_QLineEdit.text()] = self.Definition_QPlainTextEdit.toPlainText()

        with open(strJSONFile, 'w') as File:
            json.dump(JSON_Dictionary, File)
        
        self.Views_Dataframe = pd.DataFrame.from_dict(JSON_Dictionary, orient='index', columns=['Definition'])
        self.Views_Dataframe.reset_index(inplace=True)
        View_Model = Model(self.Views_Dataframe)
        self.QListView.setModel(View_Model)
