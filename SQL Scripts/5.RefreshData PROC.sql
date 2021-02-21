CREATE PROCEDURE RefreshData

AS

    --ADDING NEW ARTISTS
    DECLARE @tags VARCHAR(MAX) = STUFF( (SELECT '/' + Artists AS [text()] FROM tblNew FOR XML PATH ('') ), 1, 1, '' );

    WITH New_Artists AS (
        SELECT
            REPLACE(value, '&amp;', '&') AS Artist
        FROM
            STRING_SPLIT(@tags, '/')
        GROUP BY
            REPLACE(value, '&amp;', '&')
    )

    INSERT INTO tblArtists (Artist, Genre) (

        SELECT
            Artist,
            tblNew.Genre
        FROM
            New_Artists LEFT JOIN tblNew ON tblNew.AlbumArtist = Artist
        WHERE
            Artist NOT IN (SELECT Artist FROM tblArtists GROUP BY Artist)
        GROUP BY
            Artist,
            tblNew.Genre

    )

    --ADDING NEW ALBUMS
    INSERT INTO tblAlbums (Album, Year, Added, Artist_ID) (

        SELECT
            tblNew.Album,
            MAX(tblNew.Year) AS Year,
            MAX(tblNew.Added) AS Added,
            tblArtists.ID AS Artist_ID
        FROM
            tblNew
                INNER JOIN tblArtists
                    ON tblArtists.Artist = tblNew.AlbumArtist
                FULL OUTER JOIN tblAlbums
                    ON tblAlbums.Album = tblNew.Album
                    AND tblAlbums.Artist_ID = tblArtists.ID
        WHERE
            tblAlbums.ID IS NULL
        GROUP BY
            tblAlbums.ID,
            tblNew.Album,
            tblArtists.ID

    )

    --DELETING OLD SONGS
    DELETE FROM tblSongs
    WHERE ID IN (
        SELECT
            tblSongs.ID
        FROM
            tblOld
                INNER JOIN tblArtists
                    ON tblArtists.Artist = tblOld.AlbumArtist
                INNER JOIN tblAlbums
                    ON tblArtists.ID = tblAlbums.Artist_ID
                    AND tblOld.Album = tblAlbums.Album
                INNER JOIN tblSongs
                    ON tblSongs.Album_ID = tblAlbums.ID
                    AND tblSongs.Song = tblOld.Song
    )

    --ADDING NEW SONGS
    INSERT INTO tblSongs (Album_ID, Song, Duration, Played, Rating) (

        SELECT
            tblAlbums.ID AS Album_ID,
            tblNew.Song,
            tblNew.Duration,
            tblNew.Played,
            tblNew.Rating
        FROM
            tblNew
                INNER JOIN tblArtists
                    ON tblArtists.Artist = tblNew.AlbumArtist
                INNER JOIN tblAlbums
                    ON tblAlbums.Album = tblNew.Album
                    AND tblAlbums.Artist_ID = tblArtists.ID
                FULL OUTER JOIN tblSongs
                    ON tblSongs.Song = tblNew.Song
                    AND tblSongs.Duration = tblNew.Duration
                    AND tblSongs.Played = tblNew.Played
                    AND tblSongs.Rating = tblNew.Rating
                    AND tblSongs.Album_ID = tblAlbums.ID
        WHERE
            tblSongs.ID IS NULL

    )

    --ADDING PARTICIPATIONS
    INSERT INTO tblArtistsSongs (Song_ID, Artist_ID) (

        SELECT
            tblSongs.ID AS Song_ID,
            FeatArtist.ID AS Artist_ID
        FROM
            tblNew
                CROSS APPLY STRING_SPLIT(tblNew.Artists, '/')
                INNER JOIN tblArtists AS FeatArtist
                    ON FeatArtist.Artist = value
                INNER JOIN tblArtists AS AlbumArtist
                    ON AlbumArtist.Artist = tblNew.AlbumArtist
                INNER JOIN tblAlbums
                    ON tblAlbums.Artist_ID = AlbumArtist.ID
                    AND tblAlbums.Album = tblNew.Album
                INNER JOIN tblSongs
                    ON tblSongs.Album_ID = tblAlbums.ID
                    AND tblSongs.Song = tblNew.Song
	GROUP BY
        	tblSongs.ID,
        	FeatArtist.ID

    )

    --DELETING ALBUMS
    DELETE FROM tblAlbums
    WHERE ID IN (SELECT tblAlbums.ID FROM tblAlbums LEFT JOIN tblSongs ON tblSongs.Album_ID = tblAlbums.ID GROUP BY tblAlbums.ID, tblAlbums.Album HAVING COUNT(tblSongs.ID) = 0)

    --DELETING ARTISTS
    DELETE FROM tblArtists
    WHERE ID IN (SELECT tblArtists.ID FROM tblArtists LEFT JOIN tblArtistsSongs ON tblArtists.ID = tblArtistsSongs.Artist_ID LEFT JOIN tblAlbums ON tblArtists.ID = tblAlbums.Artist_ID GROUP BY tblArtists.ID HAVING COUNT(tblArtistsSongs.Song_ID) = 0 AND COUNT(tblAlbums.ID) = 0)

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
    INSERT INTO tblRaw (Album, Duration, Year, Song, Rating, Genre, AlbumArtist, Added, Played, Artists) (

        SELECT
            tblNew.Album,
            tblNew.Duration,
            tblNew.Year,
            tblNew.Song,
            tblNew.Rating,
            tblNew.Genre,
            tblNew.AlbumArtist,
            tblNew.Added,
            tblNew.Played,
            tblNew.Artists
        FROM
            tblNew

    )

    --EMPTYING NEW AND OLD TABLES
    DELETE FROM tblNew
    DELETE FROM tblOld

    --LOG CYCLE
    INSERT INTO tblLog VALUES (GETDATE())