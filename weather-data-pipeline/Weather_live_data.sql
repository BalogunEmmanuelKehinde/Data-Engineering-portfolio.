	 CREATE DATABASE IF NOT EXISTS live_data;
     USE live_data;
     
     CREATE TABLE weather(
		id INT AUTO_INCREMENT PRIMARY KEY,
        city VARCHAR(50),
        temperature FLOAT,
        humidity INT,
        description VARCHAR(100),
        timestamp DATETIME DEFAULT
	CURRENT_TIMESTAMP
    );
    SELECT*FROM weather;
    SHOW TABLES;
    SELECT*FROM weather;
    ALTER TABLE weather ADD COLUMN city VARCHAR(50);
    
    select*from weather order by timestamp desc;