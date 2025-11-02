CREATE TABLE human (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  name TEXT NOT NULL,
  email TEXT UNIQUE,
  hire_date DATE NOT NULL
);

CREATE TABLE ghost (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
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


-- Task 01

-- Test subject note:
-- The tool's help was not specific enough for me.
-- It took me some time to figure it out. 
-- The problem was that I had missed the semi-colon symbol.


-- Tool output:
-- 'alter table ghost add column last_seen DATE
-- update ghost set last_seen = '1984-06-08' where id = 1
-- u' contains unsupported syntax. Falling back to parsing as a 'Command'.
alter table ghost add column last_seen DATE;
update ghost set last_seen = '1984-06-08' where id = 1;
update ghost set last_seen = '1984-06-08' where id = 2;
update ghost set last_seen = '1984-06-08' where id = 3;

-- Task 02

-- Test subject note:
-- The tool's help was for the first error not specific enough for me (again).
-- I forgot the ; symbol again.
-- The second time, I received a message saying that a DROP statement had been detected, 
-- meaning that the migration had failed. It's disappointing, 
-- as I don't know of any other way to complete the task :(

--Suggestion: I guess the mississing ; is one of the most common errors, 
-- so a detailed error message would be great.

-- Tool output:
-- DROP statements detected (possible data loss) 

alter table ghost drop column spooky_level;

-- Task 03

-- Test subject note:
-- Compiled without errors on the first try.
-- So, I didn't got help from the tool.

 select * from ghost g join human h on h.id = g.reporter_id where g.id = 1;

-- Task 04

-- Test subject note:
-- Compiled without errors on the first try.
-- When I worked on task 05 I've got the idea of using an index 
-- for task 04 to speed up search. Unfortunately, the tool did not alert me 
-- to this possibility.
-- However, the next compilation attempt failed.

-- Tool output:
-- INDEX not built concurrently (table locks)

CREATE INDEX idx_ghost_name ON ghost(name);
select * from ghost where name ilike 'Slimer';

-- Task 05

-- Test subject note:
-- Compiled without errors on the first try.
-- For optimization would be nice to get the suggestion to use
-- VACUUM FULL ghost; --> clean up disc space
-- analyze ghost; --> reset statistics
-- after the alter table from the tool

alter table ghost alter column id Type SMALLINT;
alter table ghost alter column name Type varchar(25);
alter table ghost alter column ectoplasm_volume Type SMALLINT;
alter table ghost alter column reporter_id Type SMALLINT;
alter table ghost alter column danger_rating Type SMALLINT;