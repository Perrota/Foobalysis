CREATE TABLE tblArtists(
    ID INT IDENTITY PRIMARY KEY,
    Artist VARCHAR(75),
    Genre VARCHAR(25),
    Type VARCHAR(20),
    Sex VARCHAR(6)
)

CREATE TABLE tblAlbums(
    ID INT IDENTITY PRIMARY KEY,
    Album VARCHAR(75),
    Year SMALLINT,
    Added DATE,
    Artist_ID INT FOREIGN KEY REFERENCES tblArtists(ID) ON DELETE CASCADE,
)

CREATE TABLE tblSongs(
    ID INT IDENTITY PRIMARY KEY,
    Album_ID INT FOREIGN KEY REFERENCES tblAlbums(ID) ON DELETE CASCADE,
    Song VARCHAR(100),
    Duration TIME,
    Played SMALLINT,
    Rating TINYINT
)

CREATE TABLE tblArtistsSongs(
    Artist_ID INT,
    Song_ID INT FOREIGN KEY REFERENCES tblSongs(ID) ON DELETE CASCADE
)

CREATE TABLE tblRaw(
    ID INT IDENTITY PRIMARY KEY,
    Album VARCHAR(MAX),
    Duration TIME,
    Year SMALLINT,
    Song VARCHAR(MAX),
    Rating TINYINT,
    Genre VARCHAR(MAX),
    AlbumArtist VARCHAR(MAX),
    Added DATE,
    Played SMALLINT,
    Artists VARCHAR(MAX)
)

CREATE TABLE tblOld(
    ID INT IDENTITY PRIMARY KEY,
    Album VARCHAR(MAX),
    Duration TIME,
    Year SMALLINT,
    Song VARCHAR(MAX),
    Rating TINYINT,
    Genre VARCHAR(MAX),
    AlbumArtist VARCHAR(MAX),
    Added DATE,
    Played SMALLINT,
    Artists VARCHAR(MAX)
)

CREATE TABLE tblNew(
    ID INT IDENTITY PRIMARY KEY,
    Album VARCHAR(MAX),
    Duration TIME,
    Year SMALLINT,
    Song VARCHAR(MAX),
    Rating TINYINT,
    Genre VARCHAR(MAX),
    AlbumArtist VARCHAR(MAX),
    Added DATE,
    Played SMALLINT,
    Artists VARCHAR(MAX)
)

CREATE TABLE tblLog(
    TimeStamp DATETIME PRIMARY KEY
)