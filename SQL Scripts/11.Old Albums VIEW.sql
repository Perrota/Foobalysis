CREATE VIEW viewOldAlbums AS

    SELECT
        tblAlbums.ID,
        tblAlbums.Album
    FROM
        tblAlbums
            LEFT JOIN tblSongs ON tblSongs.Album_ID = tblAlbums.ID
    GROUP BY
        tblAlbums.ID,
        tblAlbums.Album
    HAVING
        COUNT(tblSongs.ID) = 0
        