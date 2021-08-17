CREATE VIEW viewNewSongs AS

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
