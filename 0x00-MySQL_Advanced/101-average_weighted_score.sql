-- Procedure that computes and store the average weighted score
-- for all students

-- Procedure that computes and store the average weighted score for
-- a student with the user_id
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;
-- Change the delimiter
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(p_user_id INT)
BEGIN
    DECLARE weighted_scores FLOAT;
    DECLARE total_weights INT DEFAULT 0;

    -- Compute the weighted score for all assignments
    -- and the total weight of all assignments 
    SELECT SUM(projects.weight * corrections.score), SUM(projects.weight)
        INTO weighted_scores, total_weights
        FROM corrections INNER JOIN projects
            ON corrections.project_id = projects.id
        WHERE corrections.user_id = p_user_id;

    -- Compute the average weighted score and save it in the user table
    IF total_weights != 0 AND total_weights IS NOT NULL THEN
        UPDATE users SET average_score = weighted_scores / total_weights
        WHERE id = p_user_id;
    END IF;
END $$

-- DROP the Procedure if exists
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
-- Create the Procedure
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    -- Call ComputeAverageWeightedScoreForUser for each user
    DECLARE finshed BOOLEAN DEFAULT FALSE;
    DECLARE user_id INT;
    DECLARE cur CURSOR FOR SELECT id FROM users;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET finshed = TRUE;
    
    OPEN cur;
    cal_Wavg: LOOP
        FETCH cur INTO user_id;
        IF finshed THEN
            LEAVE cal_Wavg;
        END IF;
        CALL ComputeAverageWeightedScoreForUser(user_id);
    END LOOP;
    CLOSE cur;
END $$
-- Reset the delimiter
DELIMITER ;
