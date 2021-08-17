CREATE VIEW viewNewArtists AS

WITH tblSplitted AS (
    SELECT
        REPLACE(value, '&amp;', '&') AS Artist
    FROM
        STRING_SPLIT(STUFF( (SELECT '/' + Artists AS [text()] FROM tblNew FOR XML PATH ('') ), 1, 1, '' ), '/')
    GROUP BY
        REPLACE(value, '&amp;', '&')
)

SELECT
    Artist,
    tblNew.Genre
FROM
    tblSplitted LEFT JOIN tblNew ON tblNew.AlbumArtist = Artist
WHERE
    Artist NOT IN (SELECT Artist FROM tblArtists GROUP BY Artist)
GROUP BY
    Artist,
    tblNew.Genre
