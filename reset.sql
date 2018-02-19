INSERT OR IGNORE INTO reset (user_id, conf_id, date, relation_id) 
VALUES ('124317807', '-1001233797421', '1517706063', (SELECT MAX(rowid) FROM relations));

        SELECT w.word, COUNT(*) as count FROM relations r 
        LEFT JOIN word w ON w.id = r.word_id
        LEFT JOIN `user` u ON u.id = r.user_id
        WHERE u.id = '124317807' AND
        r.conf_id = '-1001233797421' 
		AND r.id > (SELECT IFNULL(MAX(relation_id), 0) from reset where user_id = '124317807')
        GROUP BY w.word
        ORDER BY count DESC
        LIMIT 10;
		
SELECT MAX(relation_id) from reset where user_id = '124317807';