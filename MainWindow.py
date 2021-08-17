#! C:\Users\Marcelo\Documents\Documentos\Portfolio\Access\Musica2\env37\Scripts\python.exe

from PyQt5 import QtCore, QtGui, QtWidgets
from os import path, startfile
from SQLServer import Server
from FoobarDatabase import Database
import pandas as pd
import Programs
from GUI.QDialogViews import Ui_viewsDialog
from GUI.QDialogScraper import Ui_Dialog
from GUI.QDialogCommand import Ui_sqlDialog
from GUI.QDialogLogin import Ui_EntryWindow
from GUI.QDialogLock import Ui_LockDialog
from PandasModel import Model
import string
import csv

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):

        self.ThisFilePath_String = path.dirname(__file__)

        # Window
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(541, 539)
        MainWindow.setWindowTitle("Musica")
        MainWindow.setWindowIcon(QtGui.QIcon(path.join(self.ThisFilePath_String, 'fobalisis.ico')))
        self.CentralWidget = QtWidgets.QWidget(MainWindow)
        self.CentralWidget.setObjectName("CentralWidget")
        MainWindow.setCentralWidget(self.CentralWidget)

        # Set up menubar
        QMenuBar = QtWidgets.QMenuBar(MainWindow)
        QMenuBar.setGeometry(QtCore.QRect(0, 0, 541, 21))
        QMenuBar.setObjectName("QMenuBar")
        MainWindow.setMenuBar(QMenuBar)

        # Add menus to the menubar
        Interactions_QMenu = QtWidgets.QMenu(QMenuBar)
        Interactions_QMenu.setObjectName("Interactions_QMenu")
        Interactions_QMenu.setTitle("Interactions")
        QMenuBar.addAction(Interactions_QMenu.menuAction())

        View_QMenu = QtWidgets.QMenu(QMenuBar)
        View_QMenu.setObjectName("View_QMenu")
        View_QMenu.setTitle("View")
        QMenuBar.addAction(View_QMenu.menuAction())

        Tools_QMenu = QtWidgets.QMenu(QMenuBar)
        Tools_QMenu.setObjectName("Tools_QMenu")
        Tools_QMenu.setTitle("Tools")
        QMenuBar.addAction(Tools_QMenu.menuAction())

        # Generate CSV button config
        Scrape_QAction = QtWidgets.QAction(MainWindow)
        Scrape_QAction.setObjectName("Scrape_QAction")
        Scrape_QAction.setText("Scrape Data")
        Scrape_QAction.triggered.connect(self.Scrape_QAction_onButtonClick)

        # Video player button config
        self.PlayVideo_QAction = QtWidgets.QAction(MainWindow)
        self.PlayVideo_QAction.setObjectName("PlayVideo_QAction")
        self.PlayVideo_QAction.setText("Enable Video Player")
        self.VideoPlaying_Boolean = False
        self.PlayVideo_QAction.triggered.connect(self.PlayVideo_QAction_onButtonClick)

        # Open dash button config
        OpenDashboard_QAction = QtWidgets.QAction(MainWindow)
        OpenDashboard_QAction.setObjectName("OpenDashboard_QAction")
        OpenDashboard_QAction.setText("Open Music Dashboard")
        OpenDashboard_QAction.triggered.connect(self.OpenDashboard_QAction_onButtonClick)

        # Run command button config
        RunCMD_QAction = QtWidgets.QAction(MainWindow)
        RunCMD_QAction.setObjectName("RunCMD_QAction")
        RunCMD_QAction.setText("Run Command...")
        RunCMD_QAction.triggered.connect(self.RunCMD_QAction_onButtonClick)

        # Find dupes button config
        self.FindDupes_QAction = QtWidgets.QAction(MainWindow)
        self.FindDupes_QAction.setObjectName("FindDupes_QAction")
        self.FindDupes_QAction.setText("Potential Duplicates")
        self.FindDupes_QAction.triggered.connect(self.FindDupes_QAction_onButtonClick)

        # Custom View button config
        CustomView_QAction = QtWidgets.QAction(MainWindow)
        CustomView_QAction.setObjectName("CustomView_QAction")
        CustomView_QAction.setText("Custom View...")
        CustomView_QAction.triggered.connect(self.CustomView_QAction_onButtonClick)

        # Locks button config
        Lock_QAction = QtWidgets.QAction(MainWindow)
        Lock_QAction.setObjectName("Lock_QAction")
        Lock_QAction.setText("Lock albums")
        Lock_QAction.triggered.connect(self.Lock_QAction_onButtonClick)

        # Add buttons to the Interactions menu
        Interactions_QMenu.addAction(Scrape_QAction)
        Interactions_QMenu.addAction(self.PlayVideo_QAction)
        Interactions_QMenu.addAction(OpenDashboard_QAction)
        Interactions_QMenu.addAction(RunCMD_QAction)

        # Add buttons to the View menu
        View_QMenu.addAction(self.FindDupes_QAction)
        View_QMenu.addAction(CustomView_QAction)

        # Add button to the Tool menu
        Tools_QMenu.addAction(Lock_QAction)

        # Database frame
        MusicDatabase_QGroupBox = QtWidgets.QGroupBox(self.CentralWidget)
        MusicDatabase_QGroupBox.setGeometry(QtCore.QRect(30, 10, 481, 131))
        MusicDatabase_QGroupBox.setObjectName("MusicDatabase_QGroupBox")
        MusicDatabase_QGroupBox.setTitle("Music Database")

        # Online label
        self.Online_QLabel = QtWidgets.QLabel(MusicDatabase_QGroupBox)
        self.Online_QLabel.setGeometry(QtCore.QRect(10, 20, 121, 21))
        self.Online_QLabel.setObjectName("Online_QLabel")
        self.Online_QLabel.setText("The database is offline.")

        # Artist label
        self.Artists_QLabel = QtWidgets.QLabel(MusicDatabase_QGroupBox)
        self.Artists_QLabel.setGeometry(QtCore.QRect(10, 40, 191, 21))
        self.Artists_QLabel.setObjectName("Artists_QLabel")

        # Album label
        self.Albums_QLablel = QtWidgets.QLabel(MusicDatabase_QGroupBox)
        self.Albums_QLablel.setGeometry(QtCore.QRect(10, 60, 191, 21))
        self.Albums_QLablel.setObjectName("Albums_QLablel")

        # Song label
        self.Songs_QLabel = QtWidgets.QLabel(MusicDatabase_QGroupBox)
        self.Songs_QLabel.setGeometry(QtCore.QRect(10, 80, 191, 21))
        self.Songs_QLabel.setObjectName("Songs_QLabel")

        # SongArtist label
        self.SongsArtists_QLabel = QtWidgets.QLabel(MusicDatabase_QGroupBox)
        self.SongsArtists_QLabel.setGeometry(QtCore.QRect(10, 100, 291, 21))
        self.SongsArtists_QLabel.setObjectName("SongsArtists_QLabel")

        # Progress bar
        self.QProgressBar = QtWidgets.QProgressBar(self.CentralWidget)
        self.QProgressBar.setObjectName("QProgressBar")
        self.QProgressBar.setGeometry(QtCore.QRect(30, 150, 481, 23))
        self.QProgressBar.setProperty("value", 0)
        self.QProgressBar.setMaximum(26)

        # Grid
        self.QTableView = QtWidgets.QTableView(self.CentralWidget)
        self.QTableView.setEnabled(True)
        self.QTableView.setGeometry(QtCore.QRect(20, 180, 501, 271))
        self.QTableView.setObjectName("QTableView")

        # Layout for all the CMBs
        Layout_QWidget = QtWidgets.QWidget(self.CentralWidget)
        Layout_QWidget.setGeometry(QtCore.QRect(30, 460, 481, 25))
        Layout_QWidget.setObjectName("Layout_QWidget")
        Layout_QHBoxLayout = QtWidgets.QHBoxLayout(Layout_QWidget)
        Layout_QHBoxLayout.setContentsMargins(0, 0, 0, 0)
        Layout_QHBoxLayout.setObjectName("Layout_QHBoxLayout")

        # Comboboxes and update button
        self.Genre_QComboBox = QtWidgets.QComboBox(self.CentralWidget)
        self.Genre_QComboBox.setObjectName("Genre_QComboBox")
        Layout_QHBoxLayout.addWidget(self.Genre_QComboBox)
        
        self.Type_QComboBox = QtWidgets.QComboBox(self.CentralWidget)
        self.Type_QComboBox.setObjectName("Type_QComboBox")
        Layout_QHBoxLayout.addWidget(self.Type_QComboBox)

        self.Sex_QComboBox = QtWidgets.QComboBox(self.CentralWidget)
        self.Sex_QComboBox.setObjectName("Sex_QComboBox")
        Layout_QHBoxLayout.addWidget(self.Sex_QComboBox)

        self.Update_QPushButton = QtWidgets.QPushButton(self.CentralWidget)
        self.Update_QPushButton.setObjectName("Update_QPushButton")
        self.Update_QPushButton.setText("Update")
        self.Update_QPushButton.clicked.connect(self.Update_QPushButton_onButtonClick)
        Layout_QHBoxLayout.addWidget(self.Update_QPushButton)

        # Status bar config and installation
        self.QStatusBar = QtWidgets.QStatusBar(MainWindow)
        self.QStatusBar.setObjectName("QStatusBar")
        MainWindow.setStatusBar(self.QStatusBar)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Open QLogin and hide this one
        self.open_qlogin()
    
    def Scrape_QAction_onButtonClick(self):
        QDialog = QtWidgets.QDialog()
        ui = Ui_Dialog()
        ui.setupUi(QDialog, self.dbConn)
        QDialog.show()
        QDialog.exec_()

    def PlayVideo_QAction_onButtonClick(self):
        if self.VideoPlaying_Boolean:
            self.Player_QThread.terminate()
            self.VideoPlaying_Boolean = False
            self.PlayVideo_QAction.setText("Enable Video Player")
        elif not self.VideoPlaying_Boolean:
            self.Player_QThread = VideoPlayer_QThread()
            self.Player_QThread.start()
            self.VideoPlaying_Boolean = True
            self.PlayVideo_QAction.setText("Disable Video Player")

    def OpenDashboard_QAction_onButtonClick(self):
        startfile(path.join(self.ThisFilePath_String, 'FoobalysisBI4.pbix'))

    def RunCMD_QAction_onButtonClick(self):
        sqlDialog = QtWidgets.QDialog()
        ui = Ui_sqlDialog()
        ui.setupUi(sqlDialog, self.dbConn)
        sqlDialog.show()
        sqlDialog.exec_()

    def FindDupes_QAction_onButtonClick(self):
        self.Duplicates_Thread = DuplicateFinder_QThread(self.dbConn)
        self.Duplicates_Thread.CountChanged_pyqtSignal.connect(self.FindDupes_QAction_onUpdate)
        self.Duplicates_Thread.Finished_pyqtSignal.connect(self.FindDupes_QAction_onFinish)
        self.Duplicates_Thread.start()
        self.FindDupes_QAction.setText("Show All")
        self.Genre_QComboBox.setEnabled(False)
        self.Type_QComboBox.setEnabled(False)
        self.Sex_QComboBox.setEnabled(False)
        self.Update_QPushButton.setEnabled(False)

    def FindDupes_QAction_onUpdate(self, Value):
        self.QProgressBar.setValue(Value)

    def FindDupes_QAction_onFinish(self):

        # Change the table view
        self.Model = Model(self.Duplicates_Thread.df)
        self.QTableView.setModel(self.Model)
        self.QTableView.resizeColumnsToContents()
        self.QTableView.resizeRowsToContents()

        self.FindDupes_QAction_onUpdate(0)
        self.Update_QPushButton.setText("Not Duplicate")
        self.Update_QPushButton.setEnabled(True)

    def CustomView_QAction_onButtonClick(self):
        
        def viewDialog_onUpdate():
            self.Model = Model(ui.df)
            self.QTableView.setModel(self.Model)
            self.QTableView.resizeColumnsToContents()
            self.QTableView.resizeRowsToContents()
            self.Genre_QComboBox.setEnabled(False)
            self.Type_QComboBox.setEnabled(False)
            self.Sex_QComboBox.setEnabled(False)
            self.Update_QPushButton.setEnabled(False)
        
        viewDialog = QtWidgets.QDialog()
        ui = Ui_viewsDialog()
        ui.setupUi(viewDialog)
        ui.set_connection(self.tblArtists.Connection)
        ui.SQLstatement.connect(viewDialog_onUpdate)
        viewDialog.show()
        viewDialog.exec_()

    def Lock_QAction_onButtonClick(self):
        lockDialog = QtWidgets.QDialog()
        ui = Ui_LockDialog()
        ui.setupUi(lockDialog, self.dbConn)
        lockDialog.show()
        lockDialog.exec_()

    def Update_QPushButton_onButtonClick(self):

        def get_selected_IDs():
            Indexes_List = self.QTableView.selectedIndexes()
            Rows_List = [Index.row() for Index in Indexes_List]
            Rows_List = list( set( Rows_List ) )
            IDs_List = [self.QTableView.model().index(Row, 0).data() for Row in Rows_List]
            return (IDs_List, Rows_List)
        
        def show_popup(number_of_updates):
            MsgBox_QMessageBox = QtWidgets.QMessageBox()
            MsgBox_QMessageBox.setWindowTitle('Update')
            MsgBox_QMessageBox.setWindowIcon(QtGui.QIcon(path.join(self.ThisFilePath_String, 'foobalisis.ico')))
            MsgBox_QMessageBox.setText(f'{number_of_updates} record(s) have been updated correctly.')
            MsgBox_QMessageBox.setIcon(QtWidgets.QMessageBox.Information)
            MsgBox_QMessageBox.exec_()

        def update_model(lstRows, Genre, Type, Sex):
            for row in lstRows:
                self.Model.setData(self.QTableView.model().index(row, 2), Genre)
                self.Model.setData(self.QTableView.model().index(row, 3), Type)
                self.Model.setData(self.QTableView.model().index(row, 4), Sex)

        lstIDs, lstRows = get_selected_IDs()
        if len(lstRows) > 0:
            if self.Update_QPushButton.text() == "Update":
                    self.tblArtists.bulk_artist_update( lstIDs, self.Genre_QComboBox.currentText(), self.Type_QComboBox.currentText(), self.Sex_QComboBox.currentText() )
                    show_popup(len(lstIDs))
                    update_model(lstRows, self.Genre_QComboBox.currentText(), self.Type_QComboBox.currentText(), self.Sex_QComboBox.currentText())
            elif self.Update_QPushButton.text() == "Not Duplicate":
                lstArtists = [self.QTableView.model().index(row, 1).data() for row in lstRows]
                lstDuplicates = [self.QTableView.model().index(row, 2).data() for row in lstRows]
                strPathFile = path.join(self.ThisFilePath_String, 'NotDuplicates.csv')
                with open(strPathFile, 'a', encoding='utf-8') as f:
                    dupe_writer = csv.writer(f, delimiter=',', quotechar='"', lineterminator='\n')
                    for x in range(len(lstArtists)):
                        dupe_writer.writerow([lstArtists[x], lstDuplicates[x]])
                    show_popup(len(lstRows))
                    self.Model.drop_ids(lstIDs)
    
    def open_qlogin(self):

        def QLogin_OnUpdate():
            self.load_information(self.ui.Server_String, self.ui.Database_String)

        QDialog = QtWidgets.QDialog()
        self.ui = Ui_EntryWindow()
        self.ui.setupUi(QDialog)
        self.ui.LoadData_pyqtSignal.connect(QLogin_OnUpdate)
        QDialog.show()
        QDialog.exec_()

    def load_information(self, ServerName, DatabaseName):

        # Load Tables
        self.dbConn = Server(ServerName, DatabaseName)
        self.dbConn.connect()
        db = Database(self.dbConn)

        self.tblArtists = db.load_table('tblArtists')
        self.tblAlbums = db.load_table('tblAlbums')
        self.tblSongs = db.load_table('tblSongs')
        self.tblArtistsSongs = db.load_table('tblArtistsSongs')

        # Text indicators
        self.Online_QLabel.setText("The database is online.")
        self.Artists_QLabel.setText(f"There are {self.tblArtists.count_records()} artists in the database.")
        self.Albums_QLablel.setText(f"There are {self.tblAlbums.count_records()} albums in the database.")
        self.Songs_QLabel.setText(f"There are {self.tblSongs.count_records()} songs in the database.")
        self.SongsArtists_QLabel.setText(f"There are {self.tblArtistsSongs.count_records()} pairs of songs-artists data in the database.")

        # Table data
        CommonArtists_DataFrame = pd.read_sql('SELECT * FROM viewMostAppArtists ORDER BY Appearances DESC', self.dbConn.Connection)
        self.Model = Model(CommonArtists_DataFrame.iloc[:, :5])
        self.QTableView.setModel(self.Model)
        self.QTableView.resizeColumnsToContents()
        self.QTableView.setColumnWidth(1, 180)
        self.QTableView.resizeRowsToContents()

        # Comboboxes
        self.Genre_QComboBox.addItems(self.tblArtists.get_genre_list())
        self.Type_QComboBox.addItems(self.tblArtists.get_type_list())
        self.Sex_QComboBox.addItems(self.tblArtists.get_sex_list())

        # Status Bar
        self.QStatusBar.showMessage(f'Last Update: {db.get_last_scrape()}')


class VideoPlayer_QThread(QtCore.QThread):

    def __init__(self):
        QtCore.QThread.__init__(self)
    
    def __del__(self):
        self.wait()
    
    def run(self):
        Foobar = Programs.foobar2000(OpenDelay=3)
        Foobar.play_video()

class DuplicateFinder_QThread(QtCore.QThread):

    CountChanged_pyqtSignal = QtCore.pyqtSignal(int)
    Finished_pyqtSignal = QtCore.pyqtSignal(bool)
    
    def __init__(self, MusicDatabaseConnection):
        QtCore.QThread.__init__(self)
        self.dbConn = MusicDatabaseConnection

    def run(self):
        
        # Fuzzie matching
        Letters_List = list(string.ascii_uppercase)
        Dataframes_List = []
        for Letter in Letters_List:
            LetterDupes_Dataframe = self.dbConn.find_dupes(Letter)
            Dataframes_List.append(LetterDupes_Dataframe)
            self.CountChanged_pyqtSignal.emit(len(Dataframes_List))
        Concated_Dataframe = pd.concat(Dataframes_List)
        Concated_Dataframe.sort_values('Ratio', ascending=False, inplace=True)
        Concated_Dataframe.reset_index(inplace=True)
        
        # Existing marked
        DuplicatesFilePath_String = path.join(path.dirname(__file__), 'NotDuplicates.csv')
        NotDuplicates_Dataframe = pd.read_csv(DuplicatesFilePath_String, sep=',', encoding='utf-8', header=None)

        # Left anti join
        self.df = Concated_Dataframe.loc[
            (~Concated_Dataframe['Artist'].isin(NotDuplicates_Dataframe.iloc[:, 0]))
            &
            (~Concated_Dataframe['Ratio'].isin(NotDuplicates_Dataframe.iloc[:, 1]))
        ]

        self.Finished_pyqtSignal.emit(True)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    QMainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(QMainWindow)
    QMainWindow.show()
    sys.exit(app.exec_())
