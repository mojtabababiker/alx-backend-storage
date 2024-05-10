-- Cereate trigger for items quantity table to decrase quantity when item is sold
-- DROP the trigger if it exists
DROP TRIGGER IF EXISTS decrease_quantity;
-- Change the delimiter for the trigger
 DELIMITER ??
 CREATE TRIGGER decrease_quantity AFTER INSERT ON orders
    FOR EACH ROW
    BEGIN
        UPDATE items
        SET quantity = quantity - NEW.number
        WHERE name = NEW.item_name;
    END ??
-- Reset the delimiter
DELIMITER ;
