-- Creating an index on names table with first letter of name column
CREATE INDEX idx_name_first ON names (name(1));
