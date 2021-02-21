from PyQt5 import QtCore, QtGui, QtWidgets
from os import path

class Ui_Dialog(object):

    def setupUi(self, Dialog, dbConn):

        self.dbConn = dbConn

        # Window
        Dialog.setObjectName("Dialog")
        Dialog.setFixedSize(242, 255)
        Dialog.setWindowIcon(QtGui.QIcon(path.join(path.dirname(__file__), 'fobalisis.ico')))
        Dialog.setWindowTitle("Library Scraper")

        # Frame
        Mode_QGroupBox = QtWidgets.QGroupBox(Dialog)
        Mode_QGroupBox.setGeometry(QtCore.QRect(20, 20, 201, 71))
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
        Path_QLabel.setGeometry(QtCore.QRect(20, 100, 47, 13))
        Path_QLabel.setObjectName("Path_QLabel")
        Path_QLabel.setText("Path:")
        self.Path_QLineEdit = QtWidgets.QLineEdit(Dialog)
        self.Path_QLineEdit.setEnabled(False)
        self.Path_QLineEdit.setGeometry(QtCore.QRect(20, 120, 161, 20))
        self.Path_QLineEdit.setObjectName("Path_QLineEdit")
        self.Path_QToolButton = QtWidgets.QToolButton(Dialog)
        self.Path_QToolButton.setEnabled(False)
        self.Path_QToolButton.setGeometry(QtCore.QRect(190, 120, 25, 19))
        self.Path_QToolButton.setObjectName("Path_QToolButton")
        self.Path_QToolButton.setText("...")
        self.Path_QToolButton.clicked.connect(self.Path_QToolButton_onClicked)

        # Progress bar
        self.QProgressBar = QtWidgets.QProgressBar(Dialog)
        self.QProgressBar.setGeometry(QtCore.QRect(20, 150, 201, 23))
        self.QProgressBar.setMaximum(2)
        self.QProgressBar.setProperty("value", 0)
        self.QProgressBar.setTextVisible(False)
        self.QProgressBar.setObjectName("QProgressBar")

        # Failsafe
        FailSafe_QLabel = QtWidgets.QLabel(Dialog)
        FailSafe_QLabel.setGeometry(QtCore.QRect(20, 187, 47, 13))
        FailSafe_QLabel.setObjectName("FailSafe_QLabel")
        FailSafe_QLabel.setText('Fail-safe:')
        self.FailSafe_QLineEdit = QtWidgets.QLineEdit(Dialog)
        self.FailSafe_QLineEdit.setGeometry(QtCore.QRect(70, 184, 150, 20))
        self.FailSafe_QLineEdit.setObjectName('FailSafe_QLineEdit')
        self.FailSafe_QLineEdit.setText('10000')
        self.FailSafe_QLineEdit.setInputMask('0000000000000')

        # Exit button
        self.Exit_QPushButton = QtWidgets.QPushButton(Dialog)
        self.Exit_QPushButton.setGeometry(QtCore.QRect(130, 220, 75, 23))
        self.Exit_QPushButton.setObjectName("Exit_QPushButton")
        self.Exit_QPushButton.setText("Exit")
        self.Exit_QPushButton.clicked.connect(Dialog.close)

        # Generate button
        self.Start_QPushButton = QtWidgets.QPushButton(Dialog)
        self.Start_QPushButton.setGeometry(QtCore.QRect(40, 220, 75, 23))
        self.Start_QPushButton.setObjectName("Start_QPushButton")
        self.Start_QPushButton.setText("Generate")
        self.Start_QPushButton.clicked.connect(self.generate_csv)
        
        # Default mode
        self.Mode = 'Scraper'

        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def generate_csv(self):

        # Progress
        self.Start_QPushButton.setEnabled(False)
        self.Exit_QPushButton.setEnabled(False)
        self.QProgressBar.setValue(1)
        if self.FailSafe_QLineEdit.text() != "":
            self.dbConn.scrape(Method=self.Mode, FailSafeNumber=self.FailSafe_QLineEdit.text(), Location=self.Path_QLineEdit.text())
        else:
            self.dbConn.scrape(Method=self.Mode, Location=self.Path_QLineEdit.text())

        # Completion
        self.QProgressBar.setValue(2)
        self.Start_QPushButton.setEnabled(True)
        self.Exit_QPushButton.setEnabled(True)
    
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
