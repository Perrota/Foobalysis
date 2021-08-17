CREATE PROCEDURE RefreshData

AS

    --UNIQUE TIMESTAMP
    DECLARE @TimeStamp DATETIME = GETDATE()

    --ADDING NEW ARTISTS
    INSERT INTO tblLog (TimeStamp, Operation, [Value]) (

        SELECT
            @TimeStamp AS TimeStamp,
            'Artist Added' AS Operation,
            Artist AS [Values]
        FROM
            viewNewArtists

    )

    INSERT INTO tblArtists (Artist, Genre) (

        SELECT * FROM viewNewArtists

    )

    --ADDING NEW ALBUMS
    INSERT INTO tblLog (TimeStamp, Operation, [Value]) (

        SELECT
            @TimeStamp AS TimeStamp,
            'Album Added' AS Operation,
            Album AS [Values]
        FROM
            viewNewAlbums

    )

    INSERT INTO tblAlbums (Album, Year, Added, Artist_ID) (

        SELECT * FROM viewNewAlbums

    )

    --DELETING OLD SONGS
    INSERT INTO tblLog (TimeStamp, Operation, [Value])(

        SELECT
            @TimeStamp AS TimeStamp,
            'Song Deleted' AS Operation,
            Song AS [Values]
        FROM
            viewOldSongs

    )

    DELETE FROM tblSongs
    WHERE ID IN (SELECT ID FROM viewOldSongs)

    --ADDING NEW SONGS
    INSERT INTO tblLog (TimeStamp, Operation, [Value])(

        SELECT
            @TimeStamp AS TimeStamp,
            'Song Added' AS Operation,
            Song AS [Values]
        FROM
            viewNewSongs

    )

    INSERT INTO tblSongs (Album_ID, Song, Duration, Played, Rating) (

        SELECT * FROM viewNewSongs

    )

    --ADDING PARTICIPATIONS
    INSERT INTO
        tblLog (TimeStamp, Operation, [Value])
    VALUES
        (@TimeStamp, 'Participations Added', (SELECT COUNT(*) FROM viewNewFeatures))

    INSERT INTO tblArtistsSongs (Song_ID, Artist_ID) (

        SELECT * FROM viewNewFeatures

    )

    --DELETING ALBUMS
    INSERT INTO tblLog (TimeStamp, Operation, [Value])(

        SELECT
            @TimeStamp AS TimeStamp,
            'Album Removed' AS Operation,
            Album AS [Values]
        FROM
            viewOldAlbums

    )

    DELETE FROM tblAlbums
    WHERE ID IN (SELECT ID FROM viewOldAlbums)

    --DELETING ARTISTS
    INSERT INTO tblLog (TimeStamp, Operation, [Value])(

        SELECT
            @TimeStamp AS TimeStamp,
            'Artist Removed' AS Operation,
            Artist AS [Values]
        FROM
            viewOldArtists

    )

    DELETE FROM tblArtists
    WHERE ID IN (SELECT ID FROM viewOldArtists)

    --DELETING FROM RAW
    DELETE FROM tblRaw
    WHERE ID IN (
        SELECT
            tblRaw.ID
        FROM
            tblRaw INNER JOIN tblOld
                ON tblOld.Album = tblRaw.Album
                AND tblOld.Song = tblRaw.Song
                AND tblOld.AlbumArtist = tblRaw.AlbumArtist
                AND tblOld.Duration = tblRaw.Duration
    )

    --ADDING TO RAW
    DECLARE @LastID INT = (SELECT MAX(ID) FROM tblRaw)
    INSERT INTO tblRaw (ID, Album, Duration, Year, Song, Rating, Genre, AlbumArtist, Added, Played, Artists, Locked) (

        SELECT
            ROW_NUMBER() OVER (ORDER BY Song) + @LastID AS ID,
            tblNew.Album,
            tblNew.Duration,
            tblNew.Year,
            tblNew.Song,
            tblNew.Rating,
            tblNew.Genre,
            tblNew.AlbumArtist,
            tblNew.Added,
            tblNew.Played,
            tblNew.Artists,
            0 AS Locked
        FROM
            tblNew

    )

    --EMPTYING NEW AND OLD TABLES
    DELETE FROM tblNew
    DELETE FROM tblOld
