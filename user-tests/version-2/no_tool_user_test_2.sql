CREATE TABLE human (
  id BIGSERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT,
  hire_date DATE NOT NULL
);

CREATE TABLE ghost (
  id BIGSERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT,
  danger_rating BIGINT,
  spotted_at DATE NOT NULL
);

CREATE TABLE weapon (
  id BIGSERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  ghost_target_id INT,
  created_at TIMESTAMP
);

-- Requirement 1
-- Option 1: Assuming the ghost table is not the "true" source but instead is backed by a different source (e.g., datalake, -warehouse, ...)
-- -> we can safely delete data, as this table is basically just a "view" on already existing data, and dropped rows can be re-building from source
DELETE FROM ghost WHERE DATE(spotted_at) > '2020-01-01';
-- Option 2: if we cannot safely delete the data because it does not exist elsewhere we need to increase performance with other means..
-- 2.a) -> make reading data faster by building an index based on columns that are frequently filtered for (e.g., spotted_at)
-- 2.b) -> or, provide a second table (e.g., recent_ghosts) that only contains relevant entries. 
-- requires to be updated with new rows in the ghost table. Consider UPSERT, or scheduled recreation
CREATE TABLE recent_ghosts (
.....
) AS (
    SELECT
        *
    FROM
        ghost
    WHERE
        DATE(spotted_at) >= '2020-01-01'
)

-- Requirement 2
-- It is unclear how humans should be handled, that have not provided an email address yet (i.e. the table human contains rows with null or empty string values for email)
-- As long as there are entries with unset emails the not null constrain should not be enforced. 
-- customers can be pushed to provide an email from the business side (e.g., contact relevant humans)
-- Once ensured the constraint can be added
ALTER TABLE human ADD CONSTRAINT email NOT NULL; -- something like this
-- to help migration one could also think off releasing a human_v2 that enforces the constrain right away. New humans are added to this v2 while there's time to migrate existing humans


-- Requirement 3
-- we could add a unique constraint.
-- we need to be aware what should happen when there are conflicting rows (e.g., same name but differing ghost_target_id). Which one is the correct one? Or can there be multiple, that need to be aggregated? 
-- especially given that there have been copyright claims, one should check which manufacturer actually holds the rights to a name. 

-- Regarding the searchability adding an index on the weapon name could do the trick. If this is too slow one could consider a vectorized database
CREATE INDEX weapon_index ON weapon USING (name); -- pseudo code

-- Requirement 4
-- If joining both tables on the fly is too slow, a view won't suffice. Instead we can again provide a new table holding the prejoined rows.
-- the big question again is, how to deal with updates to either one of the source tables. Is daily update enough? Should we upsert values 
-- as they are changed in the source table? 

CREATE TABLE weapon_target_ghost (
.....
) AS (
    SELECT
        *
    FROM
        weapon
    LEFT JOIN ghost
        ON ghost_target_id = id
)

-- Requirement 5
-- Options to consider:
-- do we have many duplicates ? -> deduplicate
-- are we really accessing all data in our database equally frequent?
    -- e.g., are we accessing old data ? If no -> move to slower but cheaper storage and drop rows
-- optimize datatypes:
    -- e.g., is bigserial necessary? (allows up to 9223372036854775807 unique ids)
-- 