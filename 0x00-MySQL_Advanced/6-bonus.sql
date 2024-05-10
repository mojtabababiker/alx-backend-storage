-- Procedure that add a new correction for student
-- if the provided project dose not exist, it will be created
-- Drop the procedure if it exists
DROP PROCEDURE IF EXISTS addBonus;
-- Change the delimiter for the procedure
DELIMITER ??
-- create the procedure
CREATE PROCEDURE addBonus(user_id INT, project_name VARCHAR(255), score INT)
BEGIN
    -- get the project id
    DECLARE project_id INT;
    SELECT id INTO project_id FROM projects WHERE name = project_name;
    -- if the project does not exist, create it
    IF project_id IS NULL THEN
        -- add project
        INSERT INTO projects (name) VALUES (project_name);
        -- save it's id on the project_id variable  
        SET project_id = LAST_INSERT_ID();
    END IF;
    -- add correction
    INSERT INTO corrections (user_id, project_id, score) 
    VALUES (user_id, project_id, score);
END ??
-- Reset the delimiter
DELIMITER ;
