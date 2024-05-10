-- Creating an index on names table with first letter of name column and the score
CREATE INDEX idx_name_first ON names (name(1), score);
