-- CREATE NEW TABLE
-- CREATE users TABLE SCHEMA
CREATE TABLE IF NOT EXISTS users (
       `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
       `email` VARCHAR(255) NOT NULL UNIQUE,
       `name` varchar(255),
       `country` ENUM('US', 'CO', 'TN') NOT NULL DEFAULT 'US'
       );
