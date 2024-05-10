-- create a trigger for the email validation resets
-- DROP the trigger if it exists
DROP TRIGGER IF EXISTS email_validation;
-- Change the delimiter for the trigger
DELIMITER ??
-- CREATE THE email validation trigger
CREATE TRIGGER email_validation BEFORE UPDATE ON users
    FOR EACH ROW
    BEGIN
        IF NEW.email != OLD.email THEN
            IF OLD.valid_email = 1 THEN
                SET NEW.valid_email = 0;
            ELSE
                SET NEW.valid_email = 1;
            END IF;
        END IF;
    END ??
-- Reset the delimiter
DELIMITER ;
