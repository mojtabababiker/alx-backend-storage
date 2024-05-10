-- Create a function that run a safe division of two numbers
-- If the second number is 0, the function should return 0
-- drop the function if it already exists
DROP FUNCTION IF EXISTS safeDiv;
-- Change the delimiter
DELIMITER $$
-- Create the function
CREATE FUNCTION safeDiv (a INT, b INT) RETURNS FLOAT
BEGIN
    IF b = 0 THEN
        RETURN 0;
    ELSE
        RETURN a / b;
    END IF;
END$$
-- reset the delimiter
DELIMITER ;
