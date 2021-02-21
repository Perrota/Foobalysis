import pandas as pd
import datetime
from sqlalchemy import engine, sql, Table, orm
from Programs import foobar2000
from os import path
from fuzzywuzzy import fuzz

class MusicDatabaseConnection():

    """
    Represents the conection to the database and
    it's used to obtain information from it and modify it.
    It can also embody any of the tables in the database.
    """

    def __init__(self, Server, Database):
        self.Server = Server
        self.Database = Database

    def connect(self):
        try:
            Engine = engine.create_engine(f'mssql+pyodbc://{self.Server}/{self.Database}?driver=SQL+Server+Native+Client+11.0')
            self.Connection = Engine.connect()
            return True
        except:
            return False

    def repair_database(self, FileList):
        for FilePath in FileList:
            with open(FilePath, 'r') as File:
                SQLScript_String = File.read()
                self.Connection.execute(SQLScript_String)

    def check_structure(self):

        def all_tables_exist(List):
            tblOldExists_Boolean = 'tblOld' in List
            tblNewExists_Boolean = 'tblNew' in List
            tblRawExists_Boolean = 'tblRaw' in List
            tblArtistsExists_Boolean = 'tblArtists' in List
            tblSongsExists_Boolean = 'tblSongs' in List
            tblArtistsSongs_Boolean = 'tblArtistsSongs' in List
            viewAveMinutesExists_Boolean = 'viewAveMinutes' in List
            viewMostAppArtists_Boolean = 'viewMostAppArtists' in List
            tblAlbumsExists_Boolean = 'tblAlbums' in List
            tblLogExists_Boolean = 'tblLog' in List
            return all([
                tblOldExists_Boolean,
                tblNewExists_Boolean,
                tblRawExists_Boolean,
                tblArtistsExists_Boolean,
                tblSongsExists_Boolean,
                tblArtistsSongs_Boolean,
                viewAveMinutesExists_Boolean,
                tblAlbumsExists_Boolean,
                tblLogExists_Boolean
            ])

        self.Connection.execute(f"USE {self.Database}")
        ResultProxy = self.Connection.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES")
        Values_List = [RowProxy[0] for RowProxy in ResultProxy.fetchall()]
        return len(Values_List) >= 9 and all_tables_exist(Values_List)

    def run_command(self, Command):
        try:
            self.Connection.execute(Command)
            return True
        except:
            return False
    
    def get_daily_ave(self):
        MetaData = sql.schema.MetaData(self.Connection)
        viewAveMinutes_Table = Table('viewAveMinutes', MetaData, autoload=True)
        Select = sql.Select([viewAveMinutes_Table.c.Minutos])
        ResultProxy = self.Connection.execute(Select)
        Result_Tuple = ResultProxy.fetchone()
        return Result_Tuple[0]

    def get_last_scrape(self):
        MetaData = sql.schema.MetaData(self.Connection)
        tblLog_Table = Table('tblLog', MetaData, autoload=True)
        Select = sql.Select([tblLog_Table.c.TimeStamp]).order_by(tblLog_Table.c.TimeStamp.desc()).limit(1)
        ResultProxy = self.Connection.execute(Select)
        Result_Tuple = ResultProxy.fetchone()
        if Result_Tuple == None:
            return "Never"
        else:
            return Result_Tuple[0].strftime("%Y-%m-%d %H:%M:%S")

    def load_table(self, TableName):
        if TableName == "tblArtists":
            return tblArtists(self.Connection)
        elif TableName == "tblAlbums":
            return tblAlbums(self.Connection)
        elif TableName == "tblSongs":
            return tblSongs(self.Connection)
        elif TableName == "tblArtistsSongs":
            return tblArtistsSongs(self.Connection)
        else:
            return None
    
    def scrape(self, FailSafeNumber=5, Method='Scraper', Location=''):

        if Method == 'Scraper':
            Foobar = foobar2000(OpenDelay=3)
            pdSongs = Foobar.get_statistics()
        elif Method == 'Manual' and path.isfile(Location) and (Location[-3:] == 'txt' or Location[-3:] == 'csv') :
            pdSongs = pd.read_csv(Location, sep=';', encoding='utf-8')
        else:
            return 'Invalid load inputs.'

        if len(pdSongs) < int(FailSafeNumber):
            print("Seems like the data was not extracted right. Canceling update.")
            return False

        pdSongs = pdSongs.loc[(pdSongs.Rating != '?')&(pdSongs.Year != '?')]

        pdSongs.Year = pd.to_numeric(pdSongs.Year)
        pdSongs.Rating = pd.to_numeric(pdSongs.Rating)
        pdSongs.Added = pd.to_datetime(pdSongs.Added)
        pdSongs.Duration = pdSongs.Duration.apply(lambda x: datetime.datetime.strptime(x, '%H:%M:%S').time())

        pdSongs['Index'] = pdSongs.index

        pdCurrent = pd.read_sql('tblRaw', self.Connection)
        pdMerged = pdSongs.merge(pdCurrent, how='outer', on=['Album', 'Duration', 'Year', 'Song', 'Rating', 'Genre', 'AlbumArtist', 'Added', 'Played', 'Artists'])

        pdNew = pdMerged.loc[pd.isna(pdMerged.ID)]
        del pdNew['ID']
        del pdNew['Index']
        pdNew.to_sql('tblNew', self.Connection, if_exists='append', index=False)

        pdOld = pdMerged.loc[pd.isna(pdMerged.Index)]
        del pdOld['ID']
        del pdOld['Index']
        pdOld.to_sql('tblOld', self.Connection, if_exists='append', index=False)

        Session = orm.sessionmaker()
        Session.configure(bind=self.Connection)
        session = Session()

        session.execute('EXECUTE RefreshData')
        session.commit()

        return True
    
    def find_dupes(self, Letter):

        Artists_Dataframe = pd.read_sql(
            f"SELECT tblArtists.Artist, B.Artist AS PossibleMatch FROM tblArtists CROSS JOIN tblArtists AS B WHERE tblArtists.Artist LIKE '{Letter}%' AND B.Artist LIKE '{Letter}%'",
            self.Connection
        )

        Filtered_Dataframe = Artists_Dataframe.loc[Artists_Dataframe.Artist != Artists_Dataframe.PossibleMatch]

        Artists_List = Filtered_Dataframe.Artist.to_list()
        PossibleMatch_List = Filtered_Dataframe.PossibleMatch.to_list()

        Ratios_List = [fuzz.ratio(Artists_List[x], PossibleMatch_List[x]) for x in range(len(Filtered_Dataframe))]
        CompleteRatios_Dataframe = pd.DataFrame({'Artist': Artists_List, 'Match': PossibleMatch_List, 'Ratio': Ratios_List})

        FilteredRatios_Dataframe = CompleteRatios_Dataframe.loc[CompleteRatios_Dataframe.Ratio > 82.5]

        return FilteredRatios_Dataframe

class HipHopSQLtbl(MusicDatabaseConnection):

    def get_current_df(self, ColumnSelect="*"):
        Queried_DataFrame = pd.read_sql(f"SELECT {ColumnSelect} FROM {self.Table.name}", self.Connection)
        return Queried_DataFrame

    def count_records(self):
        Select = sql.Select([sql.func.count()]).select_from(self.Table)
        ResultProxy = self.Connection.execute(Select)
        Result_Tuple = ResultProxy.fetchone()
        return Result_Tuple[0]

class tblArtists(HipHopSQLtbl):

    def __init__(self, Connection):
        self.Connection = Connection
        self.Table = Table('tblArtists', sql.schema.MetaData(Connection), autoload=True)

    def get_genre_list(self):
        Select = sql.Select( [self.Table.c.Genre] ).group_by( self.Table.c.Genre )
        ResultProxy = self.Connection.execute(Select)
        Genres_List = [Tuple[0] for Tuple in ResultProxy]
        return Genres_List
    
    def get_type_list(self):
        Select = sql.Select( [self.Table.c.Type] ).group_by( self.Table.c.Type )
        ResultProxy = self.Connection.execute(Select)
        Types_List = [Tuple[0] for Tuple in ResultProxy]
        return Types_List

    def get_sex_list(self):
        Select = sql.Select( [self.Table.c.Sex] ).group_by( self.Table.c.Sex )
        ResultProxy = self.Connection.execute(Select)
        Sex_List = [Tuple[0] for Tuple in ResultProxy]
        return Sex_List

    def bulk_artist_update(self, lstIDs, Genre, Type, Sex):
        Update = self.Table.update().values(Genre=Genre, Type=Type, Sex=Sex).where(self.Table.c.ID.in_(lstIDs))
        self.Connection.execute(Update)

class tblAlbums(HipHopSQLtbl):

    def __init__(self, Connection):
        self.Connection = Connection
        self.Table = Table('tblAlbums', sql.schema.MetaData(Connection), autoload=True)
    
    def album_forecast(self):
        Select = sql.Select([sql.func.count()]).select_from(self.Table).where(self.Table.c.Year == datetime.date.today().year)
        ResultProxy = self.Connection.execute(Select)
        CountAlbumsCurrentYear_Int = ResultProxy.fetchone()[0]
        PrimerDiaDelAnio_Date = datetime.date(year=datetime.date.today().year, month=1, day=1)
        Hoy_Date = datetime.date.today()
        YearToDate_TimeDelta = Hoy_Date - PrimerDiaDelAnio_Date
        FracYearPassed_Float = YearToDate_TimeDelta.days / 365
        return round(CountAlbumsCurrentYear_Int / FracYearPassed_Float, 2)

class tblSongs(HipHopSQLtbl):

    def __init__(self, Connection):
        self.Connection = Connection
        self.Table = Table('tblSongs', sql.schema.MetaData(Connection), autoload=True)
    
    def get_days_of_playback(self):
        Select = sql.Select( [self.Table.c.Duration] )
        ResultProxy = self.Connection.execute(Select)
        Durations_List = [Tuple[0] for Tuple in ResultProxy]
        TimeDeltas_List = [datetime.timedelta(hours=Time.hour, minutes=Time.minute, seconds=Time.second) for Time in Durations_List]
        Sum_TimeDelta = sum(TimeDeltas_List, datetime.timedelta())
        TotalDays_Int = Sum_TimeDelta.days
        Seconds_Float = Sum_TimeDelta.seconds / (24*60*60)
        return TotalDays_Int + Seconds_Float

class tblArtistsSongs(HipHopSQLtbl):

    def __init__(self, Connection):
        self.Connection = Connection
        self.Table = Table('tblArtistsSongs', sql.schema.MetaData(Connection), autoload=True)
