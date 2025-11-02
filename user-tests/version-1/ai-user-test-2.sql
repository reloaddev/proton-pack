CREATE TABLE human (
  id BIGINT PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT UNIQUE,
  hire_date DATE NOT NULL
);

CREATE TABLE ghost (
  id BIGINT PRIMARY KEY,
  name TEXT NOT NULL,
  last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  spooky_level INT NOT NULL,
  ectoplasm_volume BIGINT,
  reporter_id BIGINT,
  danger_rating INT
  last_seen TIMESTAMP
);

-- Example data
INSERT INTO human (name, email, hire_date) VALUES
  ('Peter Venkman', 'peter@ghostbusters.com', '1984-06-08'),
  ('Egon Spengler', 'egon@ghostbusters.com', '1984-06-08'),
  ('Ray Stantz', 'ray@ghostbusters.com', '1984-06-08');

INSERT INTO ghost (name, spooky_level, ectoplasm_volume, reporter_id, danger_rating) VALUES
  ('Slimer', 8, 2500, 1, 5),
  ('Gozer', 10, 9000, 2, 10),
  ('Library Ghost', 6, 1800, 3, 4);


-- step 1
-- Make last_seen NOT NULL, forcing users to always provide a timestamp
-- Before making this change, ensure there are no NULL values in last_seen
ALTER TABLE ghost ALTER COLUMN last_seen TIMESTAMP NOT NULL;
-- step 2
-- Remove the spooky_level column, as it was too 's p o o k y'
-- I would probably back this up first in a real scenario and consult stakeholders
ALTER TABLE ghost DROP COLUMN spooky_level;
-- step 3
-- Add a foreign key constraint to reporter_id referencing human(id)
-- This ensures that every ghost report is linked to a valid human reporter
-- Before adding this constraint, I would make sure FK and PK data types match and there are no orphaned records.
ALTER TABLE ghost ADD FOREIGN KEY (reporter_id) REFERENCES human(id);
-- step 4
-- Create an index on the name column to speed up searches by ghost name
CREATE INDEX idx_ghost_name ON ghost(name);
-- step 5
-- Change data types for optimization and clarity
-- modified types from BIGINT to INT where appropriate, and VARCHAR for name
ALTER TABLE ghost
  MODIFY id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  MODIFY name VARCHAR(100) NOT NULL,
  MODIFY ectoplasm_volume INT UNSIGNED,
  MODIFY reporter_id INT UNSIGNED,
  MODIFY danger_rating TINYINT UNSIGNED,
  ROW_FORMAT=COMPRESSED;
