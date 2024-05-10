-- Creating a view that list all the students that have a score < 80
-- and have not attended any meeting or
-- last one was more than 30 days ago
-- DROP VIEW IF EXISTS need_meeting;
DROP VIEW IF EXISTS need_meeting;

-- Create the view
CREATE VIEW need_meeting AS
    SELECT name FROM students
    WHERE (score < 80) AND
    (last_meeting IS NULL OR 
    last_meeting < DATE_SUB(NOW(), INTERVAL 30 DAY));
