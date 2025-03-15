CREATE DATABASE cve_database;

USE cve_database;

CREATE TABLE cve_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cve_id VARCHAR(50) UNIQUE,
    source_identifier VARCHAR(255),
    published_date DATETIME,
    last_modified_date DATETIME,
    vuln_status VARCHAR(50),
    description TEXT,
    base_score FLOAT,
    access_vector VARCHAR(50),
    access_complexity VARCHAR(50),
    authentication VARCHAR(50),
    confidentiality_impact VARCHAR(50),
    integrity_impact VARCHAR(50),
    availability_impact VARCHAR(50)
);

SHOW TABLES;

DESC cve_data;

SELECT * FROM cve_data limit 10;

SELECT COUNT(*) FROM cve_data;

TRUNCATE TABLE cve_data;

SELECT * FROM cve_sync_log;

SET SQL_SAFE_UPDATES = 0;

SELECT cve_id, COUNT(*) 
FROM cve_data
GROUP BY cve_id
HAVING COUNT(*) > 1;

DELETE cve_data FROM cve_data 
JOIN (
    SELECT MIN(id) AS keep_id, cve_id 
    FROM cve_data 
    GROUP BY cve_id
) AS duplicates 
ON cve_data.cve_id = duplicates.cve_id 
WHERE cve_data.id <> duplicates.keep_id;

SELECT * FROM cve_data WHERE cve_id IS NULL OR description IS NULL;

UPDATE cve_data SET description = 'Unknown' WHERE description IS NULL;

SELECT * FROM cve_data 
WHERE cve_id NOT REGEXP '^CVE-[0-9]{4}-[0-9]{4,}$';

DELETE FROM cve_data  
WHERE cve_id NOT REGEXP '^CVE-[0-9]{4}-[0-9]{4,}$';

UPDATE cve_data 
SET description = TRIM(description);

SELECT * FROM cve_data WHERE base_score < 0 OR base_score > 10;

UPDATE cve_data 
SET base_score = NULL 
WHERE base_score < 0 OR base_score > 10;

SELECT * FROM cve_data 
WHERE published_date > last_modified_date;

UPDATE cve_data 
SET published_date = last_modified_date 
WHERE published_date > last_modified_date;

SELECT * FROM cve_data WHERE base_score < 0 OR base_score > 10;

UPDATE cve_data 
SET base_score = NULL 
WHERE base_score < 0 OR base_score > 10;

SELECT * FROM cve_data 
WHERE SUBSTRING(cve_id, 5, 4) > YEAR(CURDATE());

DELETE FROM cve_data 
WHERE SUBSTRING(cve_id, 5, 4) > YEAR(CURDATE());


SET SQL_SAFE_UPDATES = 1;
