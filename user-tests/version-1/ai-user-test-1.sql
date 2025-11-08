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
INSERT INTO human (id, name, email, hire_date) VALUES
  (1, 'Peter Venkman', 'peter@ghostbusters.com', '1984-06-08'),
  (2, 'Egon Spengler', 'egon@ghostbusters.com', '1984-06-08'),
  (3, 'Ray Stantz', 'ray@ghostbusters.com', '1984-06-08');

INSERT INTO ghost (id, name, spooky_level, ectoplasm_volume, reporter_id, danger_rating) VALUES
  (1, 'Slimer', 8, 2500, 1, 5),
  (2, 'Gozer', 10, 9000, 2, 10),
  (3, 'Library Ghost', 6, 1800, 3, 4);
    
-- 1
ALTER TABLE ghost
ADD COLUMN last_seen DATE NOT NULL DEFAULT CURRENT_DATE;

-- 2
ALTER TABLE ghost
DROP COLUMN spooky_level;

-- 3
ALTER TABLE ghost
ADD CONSTRAINT fk_ghost_reporter
FOREIGN KEY (reporter_id)
REFERENCES human(id);

-- 4
-- SELECT * FROM ghost WHERE LOWER(name) LIKE LOWER('%' || :searchTerm || '%');
SELECT * FROM ghost WHERE LOWER(name) LIKE LOWER('%Slimer%');


 -- 5
ALTER TABLE ghost
ALTER COLUMN id SET DATA TYPE INTEGER,
ALTER COLUMN ectoplasm_volume SET DATA TYPE INTEGER,
ALTER COLUMN danger_rating SET DATA TYPE SMALLINT; 
 
 \dt
 \d ghost
 \d human
