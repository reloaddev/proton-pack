CREATE TABLE human (
  id BIGINT PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT UNIQUE,
  hire_date DATE NOT NULL
);

CREATE TABLE ghost (
  id BIGINT PRIMARY KEY,
  name TEXT NOT NULL,
  spooky_level INT NOT NULL,
  ectoplasm_volume BIGINT,
  reporter_id BIGINT,
  danger_rating INT,
  last_seen TIMESTAMP
);

ALTER TABLE ghost DROP COLUMN spooky_level;

ALTER TABLE ghost ADD FOREIGN KEY (reporter) REFERENCES human(id);
-- Cool, I'd probably forget to add an index to the foreign key
CREATE INDEX ghost_reporter_idx ON ghost (reporter);

INSERT INTO ghost VALUES (1, "Slimer", 7, 1, 10, 2/11/2025);
-- With this I would never manually insert an ID number but this isn't what is focussed on.

SELECT * FROM ghost WHERE name="Slimer";

ALTER TABLE human ALTER COLUMN id SMALLINT;
ALTER TABLE ghost ALTER COLUMN id SMALLINT;
ALTER TABLE ghost ALTER COLUMN ectoplasm_volume SMALLINT;
ALTER TABLE ghost ALTER COLUMN danger_rating SMALLINT;
ALTER TABLE ghost DROP COLUMN reporter_id;
-- Since we added the foreign key, the reporter_id is becomes irrelevant. Refer to Reporter instead.
ALTER TABLE ghost ALTER COLUMN last_seen DATE;

