from PyQt5 import QtCore, QtGui, QtWidgets
from os import path

class Ui_sqlDialog(object):

    def setupUi(self, sqlDialog, dbConn):

        self.dbConn = dbConn

        # Window
        sqlDialog.setObjectName("sqlDialog")
        sqlDialog.setFixedSize(400, 95)
        sqlDialog.setWindowTitle("Run Command...")
        sqlDialog.setWindowIcon(QtGui.QIcon(path.join(path.dirname(path.dirname(__file__)), 'fobalisis.ico')))

        # Label
        Command_QLabel = QtWidgets.QLabel(sqlDialog)
        Command_QLabel.setGeometry(QtCore.QRect(20, 10, 101, 16))
        Command_QLabel.setText("Type SQL command:")
        Command_QLabel.setObjectName("Command_QLabel")

        # Textbox
        self.Command_QLineEdit = QtWidgets.QLineEdit(sqlDialog)
        self.Command_QLineEdit.setGeometry(QtCore.QRect(20, 30, 361, 20))
        self.Command_QLineEdit.setObjectName("Command_QLineEdit")
        
        # Run button
        Run_QPushButton = QtWidgets.QPushButton(sqlDialog)
        Run_QPushButton.setObjectName("Run_QPushButton")
        Run_QPushButton.setGeometry(QtCore.QRect(220, 60, 75, 23))
        Run_QPushButton.setText('Run')
        Run_QPushButton.clicked.connect(self.Run_QPushButton_onButtonClick)

        # Exit button
        Exit_QPushButton = QtWidgets.QPushButton(sqlDialog)
        Exit_QPushButton.setObjectName("Exit_QPushButton")
        Exit_QPushButton.setGeometry(QtCore.QRect(300, 60, 75, 23))
        Exit_QPushButton.setText('Exit')
        Exit_QPushButton.clicked.connect(sqlDialog.close)

        QtCore.QMetaObject.connectSlotsByName(sqlDialog)

    def Run_QPushButton_onButtonClick(self):

        def show_popup(Success):
            QMessageBox = QtWidgets.QMessageBox()
            QMessageBox.setWindowIcon(QtGui.QIcon(path.join(path.dirname(__file__), 'fobalisis.ico')))
            if Success:
                QMessageBox.setWindowTitle('Done')
                QMessageBox.setIcon(QtWidgets.QMessageBox.Information)
                QMessageBox.setText(f'The command has been executed successfully.')
            if not Success:
                QMessageBox.setWindowTitle('Error')
                QMessageBox.setIcon(QtWidgets.QMessageBox.Critical)
                QMessageBox.setText(f'The command has failed. Check for syntax errors.')
            QMessageBox.exec_()

        Command_String = self.Command_QLineEdit.text()
        Result_Boolean = self.dbConn.run_command(Command_String)
        show_popup(Result_Boolean)
