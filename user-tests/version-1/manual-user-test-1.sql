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
  danger_rating INT
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


ALTER TABLE ghost ADD last_seen TIMESTAMP DEFAULT NULL;

ALTER TABLE ghost DROP COLUMN spooky_level;

ALTER TABLE ghost
      ADD CONSTRAINT reporter_id_fk FOREIGN KEY (reporter_id) 
          REFERENCES human(id);

CREATE INDEX ghost_index ON ghost (name);

-- storage (use integer instead of bigint or something)
ALTER TABLE ghost
ALTER COLUMN ectoplasm_volume TYPE INTEGER;