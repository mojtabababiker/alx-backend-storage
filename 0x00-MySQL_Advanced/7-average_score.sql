-- Procedure thaat computes and stores the average score for a student
-- Drop the procedure if it exists
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;
-- Change the delimiter for the procedure
DELIMITER ??
-- Create the procedure
CREATE PROCEDURE ComputeAverageScoreForUser(p_user_id INT)
BEGIN
    -- Defind the variable to store the average score
    DECLARE avg_score FLOAT;
    -- Compute the average score for the user with the provided id
    SELECT AVG(score) INTO avg_score FROM corrections
    WHERE user_id = p_user_id;
    -- Store the average score in the users table
    UPDATE users SET average_score = avg_score WHERE id = p_user_id;
END ??
-- Reset the delimiter
DELIMITER ;
