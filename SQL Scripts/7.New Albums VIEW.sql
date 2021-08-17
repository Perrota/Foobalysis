CREATE VIEW viewNewAlbums AS

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