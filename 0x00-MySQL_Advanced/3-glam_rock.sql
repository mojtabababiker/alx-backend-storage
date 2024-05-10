-- Drop the function if it exists
DROP FUNCTION IF EXISTS life_span;

-- Change the delimiter for the function
DELIMITER ??

-- Create the function
CREATE FUNCTION life_span(p_band_name VARCHAR(255)) RETURNS INT
BEGIN
    -- Variable declaration for split year and formed year
    DECLARE splited YEAR;
    DECLARE formed_v YEAR;
    DECLARE lifespan INT;

    -- Select the split year and formed year from the metal_bands table
    SELECT split, formed INTO splited, formed_v
    FROM metal_bands
    WHERE band_name = p_band_name;

    -- If the split year is NULL, assume the band is still active
    SET splited = COALESCE(splited, YEAR("2022"));

    -- Calculate the band lifespan
    SET lifespan = DATEDIFF(splited, formed_v);

    -- Return the calculated lifespan
    RETURN lifespan;
END ??

-- Reset the delimiter
DELIMITER ;

-- Call the life_span procedure for all the "Glam rock" bands
SELECT band_name, life_span(band_name) AS life_span
FROM metal_bands
WHERE style = "Glam rock"
ORDER BY life_span DESC;
