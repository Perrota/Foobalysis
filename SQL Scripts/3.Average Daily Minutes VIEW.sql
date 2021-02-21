CREATE VIEW viewAveMinutes  
AS  
SELECT
    ROUND(SUM(CAST(DATEDIFF(SECOND, '00:00:00', dbo.tblSongs.Duration) AS FLOAT) / CAST(60 AS FLOAT)), 2) / DATEDIFF(DAY, DATEFROMPARTS(YEAR(GETDATE()), 1, 1), GETDATE() + 1) AS 'Minutos'
FROM
    dbo.tblAlbums INNER JOIN
        dbo.tblSongs
            ON dbo.tblSongs.Album_ID = dbo.tblAlbums.ID
WHERE
    (YEAR(dbo.tblAlbums.Added) = YEAR(GETDATE()))
GROUP BY
    YEAR(dbo.tblAlbums.Added);