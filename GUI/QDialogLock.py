from PyQt5 import QtCore, QtGui, QtWidgets
from os import path
from PandasModel import Model
import pandas as pd
import shutil
from sqlalchemy import sql, Table, MetaData

class Ui_LockDialog(object):

    CurrentPath_String = path.dirname(__file__)

    def setupUi(self, Dialog, FoobarDB):

        self.Connection = FoobarDB.Connection

        Dialog.setObjectName("Dialog")
        Dialog.setFixedSize(692, 304)
        Dialog.setWindowTitle("Lock/Unlocking Albums")
        Dialog.setWindowIcon(QtGui.QIcon(path.join(path.dirname(self.CurrentPath_String), 'fobalisis.ico')))

        Artists_QLabel = QtWidgets.QLabel(Dialog)
        Artists_QLabel.setGeometry(QtCore.QRect(20, 20, 321, 16))
        Artists_QLabel.setAlignment(QtCore.Qt.AlignCenter)
        Artists_QLabel.setObjectName("Artists_QLabel")
        Artists_QLabel.setText("Artists")

        Albums_QLabel = QtWidgets.QLabel(Dialog)
        Albums_QLabel.setGeometry(QtCore.QRect(350, 20, 321, 16))
        Albums_QLabel.setAlignment(QtCore.Qt.AlignCenter)
        Albums_QLabel.setObjectName("Albums_QLabel")
        Albums_QLabel.setText("Albums")

        Artists_Model = Model(pd.read_sql('SELECT tblArtists.ID, tblArtists.Artist FROM tblArtists INNER JOIN tblAlbums ON tblAlbums.Artist_ID = tblArtists.ID GROUP BY tblArtists.ID, tblArtists.Artist', FoobarDB.Connection))
        self.Artists_QTableView = QtWidgets.QTableView(Dialog)
        self.Artists_QTableView.setGeometry(QtCore.QRect(20, 70, 321, 192))
        self.Artists_QTableView.setObjectName("Artists_QTableView")
        self.Artists_QTableView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.Artists_QTableView.setModel(Artists_Model)
        self.Artists_QTableView.setColumnHidden(0, True)
        self.Artists_QTableView.setColumnWidth(1, 270)
        self.Artists_QTableView.resizeRowsToContents()
        self.Artists_QTableView.clicked.connect(self.Artists_QTableView_OnItemClicked)

        Albums_Model = Model(pd.read_sql("SELECT tblArtists.Artist, tblAlbums.Album, IIF(tRaw.Locked = 0, 'Unlocked', 'Locked') AS [Status] FROM tblAlbums INNER JOIN tblArtists ON tblArtists.ID = tblAlbums.Artist_ID INNER JOIN (SELECT tblRaw.AlbumArtist, tblRaw.Album, tblRaw.Locked FROM tblRaw GROUP BY AlbumArtist, Album, Locked) AS tRaw ON tRaw.AlbumArtist = tblArtists.Artist AND tRaw.Album = tblAlbums.Album", self.Connection))
        self.Album_QTableView = QtWidgets.QTableView(Dialog)
        self.Album_QTableView.setGeometry(QtCore.QRect(350, 70, 321, 192))
        self.Album_QTableView.setObjectName("Album_QTableView")
        self.Album_QTableView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.Album_QTableView.setModel(Albums_Model)
        self.Album_QTableView.setColumnHidden(0, True)
        self.Album_QTableView.setColumnWidth(1, 203)
        self.Album_QTableView.setColumnWidth(2, 60)
        self.Album_QTableView.resizeRowsToContents()

        Artists_QLineEdit = QtWidgets.QLineEdit(Dialog)
        Artists_QLineEdit.setGeometry(QtCore.QRect(20, 50, 321, 20))
        Artists_QLineEdit.setObjectName("Artists_QLineEdit")
        Artists_QLineEdit.textChanged.connect(self.Artists_QLineEdit_OnTextChanged)

        self.Albums_QLineEdit = QtWidgets.QLineEdit(Dialog)
        self.Albums_QLineEdit.setGeometry(QtCore.QRect(350, 50, 321, 20))
        self.Albums_QLineEdit.setObjectName("Albums_QLineEdit")
        self.Albums_QLineEdit.textChanged.connect(self.Albums_QLineEdit_OnTextChanged)

        Change_QPushButton = QtWidgets.QPushButton(Dialog)
        Change_QPushButton.setGeometry(QtCore.QRect(590, 270, 75, 23))
        Change_QPushButton.setObjectName("Change_QPushButton")
        Change_QPushButton.setText("Lock")
        Change_QPushButton.clicked.connect(self.Change_QPushButton_OnClick)

        QtCore.QMetaObject.connectSlotsByName(Dialog)
    
    def Artists_QLineEdit_OnTextChanged(self, Text):
        Artists_Model = Model(pd.read_sql(f"SELECT tblArtists.ID, tblArtists.Artist FROM tblArtists INNER JOIN tblAlbums ON tblAlbums.Artist_ID = tblArtists.ID WHERE tblArtists.Artist LIKE '%{Text}%' GROUP BY tblArtists.ID, tblArtists.Artist", self.Connection))
        self.Artists_QTableView.setModel(Artists_Model)
        self.Artists_QTableView.resizeRowsToContents()

    def Albums_QLineEdit_OnTextChanged(self, Text):
        Albums_Model = Model(pd.read_sql(f"SELECT tblArtists.Artist, tblAlbums.Album, IIF(tRaw.Locked = 0, 'Unlocked', 'Locked') AS [Status] FROM tblAlbums INNER JOIN tblArtists ON tblArtists.ID = tblAlbums.Artist_ID INNER JOIN (SELECT tblRaw.AlbumArtist, tblRaw.Album, tblRaw.Locked FROM tblRaw GROUP BY AlbumArtist, Album, Locked) AS tRaw ON tRaw.AlbumArtist = tblArtists.Artist AND tRaw.Album = tblAlbums.Album WHERE tblAlbums.Album LIKE '%{Text}%'", self.Connection))
        self.Album_QTableView.setModel(Albums_Model)
        self.Album_QTableView.resizeRowsToContents()
    
    def Artists_QTableView_OnItemClicked(self, ModelIndex):
        ArtistID_String = self.Artists_QTableView.model().index(ModelIndex.row(), 0).data()
        Albums_Model = Model(pd.read_sql(f"SELECT tblArtists.Artist, tblAlbums.Album, IIF(tRaw.Locked = 0, 'Unlocked', 'Locked') AS [Status] FROM tblAlbums INNER JOIN tblArtists ON tblArtists.ID = tblAlbums.Artist_ID INNER JOIN (SELECT tblRaw.AlbumArtist, tblRaw.Album, tblRaw.Locked FROM tblRaw GROUP BY AlbumArtist, Album, Locked) AS tRaw ON tRaw.AlbumArtist = tblArtists.Artist AND tRaw.Album = tblAlbums.Album WHERE tblArtists.ID = {ArtistID_String}", self.Connection))
        self.Album_QTableView.setModel(Albums_Model)
        self.Album_QTableView.resizeRowsToContents()

    def Change_QPushButton_OnClick(self):
        SelectedIndex_QModelIndex = self.Album_QTableView.selectedIndexes()[0]
        AlbumArtist_String = self.Album_QTableView.model().index(SelectedIndex_QModelIndex.row(), 0).data()
        AlbumName_String = self.Album_QTableView.model().index(SelectedIndex_QModelIndex.row(), 1).data()
        Metadata = MetaData(self.Connection)
        Raw_Table = Table('tblRaw', Metadata, autoload=True)
        UpdateQuery_String = sql.update(Raw_Table).where(Raw_Table.c.AlbumArtist == AlbumArtist_String).where(Raw_Table.c.Album == AlbumName_String).values(Locked=1)
        self.Connection.execute(UpdateQuery_String)
        QMessageBox = QtWidgets.QMessageBox()
        QMessageBox.setText("Records have been locked.\nDo you want to delete its corresponding folder too?")
        QMessageBox.setIcon(QtWidgets.QMessageBox.Question)
        QMessageBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        QMessageBox.setWindowTitle('Delete folder')
        QMessageBox.setWindowIcon(QtGui.QIcon(path.join(path.dirname(self.CurrentPath_String), 'fobalisis.ico')))
        response = QMessageBox.exec_()
        if response == QtWidgets.QMessageBox.Yes:
            Folder_String = QtWidgets.QFileDialog.getExistingDirectory()
            shutil.rmtree(Folder_String)
            QMessageBox = QtWidgets.QMessageBox()
            QMessageBox.setText("Folder deleted.")
            QMessageBox.setIcon(QtWidgets.QMessageBox.Information)
            QMessageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            QMessageBox.setWindowTitle('Done')
            QMessageBox.setWindowIcon(QtGui.QIcon(path.join(path.dirname(self.CurrentPath_String), 'fobalisis.ico')))
            QMessageBox.exec_()
            Albums_Model = Model(pd.read_sql("SELECT tblArtists.Artist, tblAlbums.Album, IIF(tRaw.Locked = 0, 'Unlocked', 'Locked') AS [Status] FROM tblAlbums INNER JOIN tblArtists ON tblArtists.ID = tblAlbums.Artist_ID INNER JOIN (SELECT tblRaw.AlbumArtist, tblRaw.Album, tblRaw.Locked FROM tblRaw GROUP BY AlbumArtist, Album, Locked) AS tRaw ON tRaw.AlbumArtist = tblArtists.Artist AND tRaw.Album = tblAlbums.Album", self.Connection))
            self.Album_QTableView.setModel(Albums_Model)
            