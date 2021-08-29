CREATE VIEW viewLastLogs AS 

(
    SELECT
        *
    FROM
        tblLog
    WHERE
        [TimeStamp] = (SELECT MAX([TimeStamp]) FROM tblLog)
)
