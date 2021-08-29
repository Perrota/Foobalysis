from PyQt5 import QtCore, QtGui, QtWidgets
from os import path
from FoobarDatabase import AppDB
from Programs import foobar2000
from PandasModel import Model
import pandas as pd

class Ui_Dialog(object):

    def setupUi(self, Dialog, AppDB):

        self.db = AppDB

        # Window
        Dialog.setObjectName("Dialog")
        Dialog.setFixedSize(431, 381)
        Dialog.setWindowIcon(QtGui.QIcon(path.join(path.dirname(path.dirname(__file__)), 'fobalisis.ico')))
        Dialog.setWindowTitle("Library Scraper")

        # Frame
        Mode_QGroupBox = QtWidgets.QGroupBox(Dialog)
        Mode_QGroupBox.setGeometry(QtCore.QRect(20, 20, 391, 71))
        Mode_QGroupBox.setObjectName("Mode_QGroupBox")
        Mode_QGroupBox.setTitle("Mode")

        # Options
        Auto_QRadioButton = QtWidgets.QRadioButton(Mode_QGroupBox)
        Auto_QRadioButton.setGeometry(QtCore.QRect(20, 30, 82, 17))
        Auto_QRadioButton.setChecked(True)
        Auto_QRadioButton.setObjectName("Auto_QRadioButton")
        Auto_QRadioButton.setText("Automatic")
        Auto_QRadioButton.clicked.connect(self.Auto_QRadioButton_onClicked)
        Manual_QRadioButton = QtWidgets.QRadioButton(Mode_QGroupBox)
        Manual_QRadioButton.setGeometry(QtCore.QRect(110, 30, 82, 17))
        Manual_QRadioButton.setObjectName("Manual_QRadioButton")
        Manual_QRadioButton.setText("Manual")
        Manual_QRadioButton.clicked.connect(self.Manual_QRadioButton_onClicked)

        # Path
        Path_QLabel = QtWidgets.QLabel(Dialog)
        Path_QLabel.setGeometry(QtCore.QRect(200, 40, 47, 13))
        Path_QLabel.setObjectName("Path_QLabel")
        Path_QLabel.setText("Path:")
        self.Path_QLineEdit = QtWidgets.QLineEdit(Dialog)
        self.Path_QLineEdit.setEnabled(False)
        self.Path_QLineEdit.setGeometry(QtCore.QRect(200, 60, 161, 20))
        self.Path_QLineEdit.setObjectName("Path_QLineEdit")
        self.Path_QToolButton = QtWidgets.QToolButton(Dialog)
        self.Path_QToolButton.setEnabled(False)
        self.Path_QToolButton.setGeometry(QtCore.QRect(370, 60, 25, 19))
        self.Path_QToolButton.setObjectName("Path_QToolButton")
        self.Path_QToolButton.setText("...")
        self.Path_QToolButton.clicked.connect(self.Path_QToolButton_onClicked)

        # Log table
        self.QTableView = QtWidgets.QTableView(Dialog)
        self.QTableView.setGeometry(QtCore.QRect(20, 140, 391, 192))
        self.QTableView.setObjectName("QTableView")

        # Progress bar
        self.QProgressBar = QtWidgets.QProgressBar(Dialog)
        self.QProgressBar.setGeometry(QtCore.QRect(20, 100, 391, 23))
        self.QProgressBar.setMaximum(3)
        self.QProgressBar.setProperty("value", 0)
        self.QProgressBar.setTextVisible(False)
        self.QProgressBar.setObjectName("QProgressBar")

        # Failsafe
        FailSafe_QLabel = QtWidgets.QLabel(Dialog)
        FailSafe_QLabel.setGeometry(QtCore.QRect(25, 344, 47, 13))
        FailSafe_QLabel.setObjectName("FailSafe_QLabel")
        FailSafe_QLabel.setText('Fail-safe:')
        self.FailSafe_QLineEdit = QtWidgets.QLineEdit(Dialog)
        self.FailSafe_QLineEdit.setGeometry(QtCore.QRect(75, 341, 150, 20))
        self.FailSafe_QLineEdit.setObjectName('FailSafe_QLineEdit')
        self.FailSafe_QLineEdit.setText('10000')
        self.FailSafe_QLineEdit.setInputMask('0000000000000')

        # Exit button
        self.Exit_QPushButton = QtWidgets.QPushButton(Dialog)
        self.Exit_QPushButton.setGeometry(QtCore.QRect(330, 340, 75, 23))
        self.Exit_QPushButton.setObjectName("Exit_QPushButton")
        self.Exit_QPushButton.setText("Exit")
        self.Exit_QPushButton.clicked.connect(Dialog.close)

        # Generate button
        self.Start_QPushButton = QtWidgets.QPushButton(Dialog)
        self.Start_QPushButton.setGeometry(QtCore.QRect(250, 340, 75, 23))
        self.Start_QPushButton.setObjectName("Start_QPushButton")
        self.Start_QPushButton.setText("Generate")
        self.Start_QPushButton.clicked.connect(self.generate_csv)
        
        # Default mode
        self.Mode = 'Scraper'

        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def generate_csv(self):

        # Initial
        Foobar = foobar2000(OpenDelay=2)

        # Progress
        self.Start_QPushButton.setEnabled(False)
        self.Exit_QPushButton.setEnabled(False)
        self.QProgressBar.setValue(1)
        if self.FailSafe_QLineEdit.text() != "":
            Foobar.scrape(self.db.Connection, FailSafeNumber=self.FailSafe_QLineEdit.text(), Location=self.Path_QLineEdit.text())
        else:
            Foobar.scrape(self.db.Connection, Method=self.Mode, Location=self.Path_QLineEdit.text())

        # Completion
        self.QProgressBar.setValue(2)
        self.Start_QPushButton.setEnabled(True)
        self.Exit_QPushButton.setEnabled(True)
        self.RefreshTableView()
        self.QProgressBar.setValue(3)
    
    def Manual_QRadioButton_onClicked(self):
        self.Path_QLineEdit.setEnabled(True)
        self.Path_QToolButton.setEnabled(True)
        self.Mode = 'Manual'
    
    def Auto_QRadioButton_onClicked(self):
        self.Path_QLineEdit.setEnabled(False)
        self.Path_QLineEdit.setText('')
        self.Path_QToolButton.setEnabled(False)
        self.Mode = 'Scraper'
    
    def Path_QToolButton_onClicked(self):
        File_Tuple = QtWidgets.QFileDialog.getOpenFileName()
        self.Path_QLineEdit.setText(File_Tuple[0])

    def RefreshTableView(self):
        df = pd.read_sql('SELECT CAST(TimeStamp AS DATE) AS TimeStamp, Operation, Value FROM viewLastLogs', self.db.Connection)
        Log_Model = Model(df)
        self.QTableView.setModel(Log_Model)
        self.QTableView.resizeColumnsToContents()
        self.QTableView.resizeRowsToContents()
