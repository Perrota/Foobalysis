CREATE VIEW viewOldSongs AS

    SELECT
        tblSongs.ID,
        tblSongs.Song
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