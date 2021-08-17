CREATE VIEW viewOldArtists AS

    SELECT
        tblArtists.ID,
        tblArtists.Artist
    FROM
        tblArtists
            LEFT JOIN tblArtistsSongs
                ON tblArtists.ID = tblArtistsSongs.Artist_ID
            LEFT JOIN tblAlbums
                ON tblArtists.ID = tblAlbums.Artist_ID
    GROUP BY
        tblArtists.ID,
        tblArtists.Artist
    HAVING
        COUNT(tblArtistsSongs.Song_ID) = 0 AND
        COUNT(tblAlbums.ID) = 0
