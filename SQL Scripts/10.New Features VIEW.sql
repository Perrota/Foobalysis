CREATE VIEW viewNewFeatures AS

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
            