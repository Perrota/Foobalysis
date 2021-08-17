from PyQt5 import QtCore, QtGui, QtWidgets
from os import path
from PandasModel import Model
import pandas as pd

class Ui_LockDialog(object):

    CurrentPath_String = path.dirname(__file__)

    def setupUi(self, Dialog, MusicDatabaseConnection):

        Dialog.setObjectName("Dialog")
        Dialog.resize(572, 304)
        Dialog.setWindowTitle("Lock/Unlocking Albums")
        Dialog.setWindowIcon(QtGui.QIcon(path.join(self.CurrentPath_String, 'fobalisis.ico')))

        self.Artists_QLabel = QtWidgets.QLabel(Dialog)
        self.Artists_QLabel.setGeometry(QtCore.QRect(20, 20, 261, 16))
        self.Artists_QLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.Artists_QLabel.setObjectName("Artists_QLabel")
        self.Artists_QLabel.setText("Artists")

        self.Albums_QLabel = QtWidgets.QLabel(Dialog)
        self.Albums_QLabel.setGeometry(QtCore.QRect(290, 20, 261, 16))
        self.Albums_QLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.Albums_QLabel.setObjectName("Albums_QLabel")
        self.Albums_QLabel.setText("Albums")

        Artists_Model = Model(pd.read_sql('SELECT tblArtists.Artist FROM tblArtists INNER JOIN tblAlbums ON tblAlbums.Artist_ID = tblArtists.ID GROUP BY tblArtists.Artist', MusicDatabaseConnection.Connection))
        Albums_Model = Model(pd.read_sql('SELECT Album From tblAlbums', MusicDatabaseConnection.Connection))

        self.Artists_QListView = QtWidgets.QListView(Dialog)
        self.Artists_QListView.setGeometry(QtCore.QRect(20, 70, 261, 192))
        self.Artists_QListView.setObjectName("Artists_QListView")
        self.Artists_QListView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.Artists_QListView.setModel(Artists_Model)

        self.Album_QListView = QtWidgets.QListView(Dialog)
        self.Album_QListView.setGeometry(QtCore.QRect(290, 70, 261, 192))
        self.Album_QListView.setObjectName("Album_QListView")
        self.Album_QListView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.Album_QListView.setModel(Albums_Model)

        self.Artists_QLineEdit = QtWidgets.QLineEdit(Dialog)
        self.Artists_QLineEdit.setGeometry(QtCore.QRect(20, 50, 261, 20))
        self.Artists_QLineEdit.setObjectName("Artists_QLineEdit")

        self.Albums_QLineEdit = QtWidgets.QLineEdit(Dialog)
        self.Albums_QLineEdit.setGeometry(QtCore.QRect(290, 50, 261, 20))
        self.Albums_QLineEdit.setObjectName("Albums_QLineEdit")

        self.Change_QPushButton = QtWidgets.QPushButton(Dialog)
        self.Change_QPushButton.setGeometry(QtCore.QRect(470, 270, 75, 23))
        self.Change_QPushButton.setObjectName("Change_QPushButton")
        self.Change_QPushButton.setText("Lock")

        QtCore.QMetaObject.connectSlotsByName(Dialog)

    # def set_connection(self, Connection):
        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
