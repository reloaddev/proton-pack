CREATE TABLE human (id BIGSERIAL PRIMARY KEY,name TEXT NOT NULL,email TEXT,hire_date DATE NOT NULL);

CREATE TABLE ghost (id BIGSERIAL PRIMARY KEY,name TEXT NOT NULL,description TEXT,danger_rating BIGINT,spotted_at DATE NOT NULL);

CREATE TABLE weapon (id BIGSERIAL PRIMARY KEY,name TEXT NOT NULL,ghost_target_id INT,created_at TIMESTAMP);

-- Task 01
CREATE INDEX CONCURRENTLY idx_ghost_active_overview ON ghost (spotted_at DESC) WHERE spotted_at >= '2020-01-01'::date;

-- Task 02
-- Before executing the ALTER TABLE command, we must handle all existing records where email is currently NULL. For now we update the NULL values with a temporary or placeholder value.
UPDATE human SET email = 'no_email_' || id || '@placeholder.com' WHERE email IS NULL;
ALTER TABLE human ALTER COLUMN email SET NOT NULL;

-- Task 03
-- If there are duplicate values in the weapon.name column in existing data, the ALTER TABLE command will fail immediately.
ALTER TABLE weapon ADD CONSTRAINT uq_weapon_name UNIQUE (name);

-- Task 04
CREATE TABLE weapon_target_ghost_summary AS SELECT w.id AS weapon_id,w.name AS weapon_name,w.created_at AS weapon_created_at,g.id AS target_ghost_id,g.name AS target_ghost_name,g.danger_rating AS target_danger_rating,g.spotted_at AS target_last_spotted FROM weapon w JOIN ghost g ON w.ghost_target_id = g.id WITH DATA;

-- Task 05
ALTER TABLE human ALTER COLUMN id TYPE INT, ALTER COLUMN email TYPE VARCHAR(255);
UPDATE ghost SET danger_rating = 0 WHERE danger_rating IS NULL;
ALTER TABLE ghost ALTER COLUMN danger_rating TYPE SMALLINT;
ALTER TABLE weapon ALTER COLUMN id TYPE INT, ALTER COLUMN ghost_target_id TYPE SMALLINT;