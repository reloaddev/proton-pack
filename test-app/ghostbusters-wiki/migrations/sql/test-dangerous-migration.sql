CREATE TABLE ghost (id INTEGER PRIMARY KEY, name TEXT, type TEXT, reporter_id INTEGER);
ALTER TABLE ghost ADD CONSTRAINT fk_reporter FOREIGN KEY (reporter_id) REFERENCES human(id);
ALTER TABLE ghost ADD COLUMN classification TEXT NOT NULL;
CREATE INDEX ON ghost(name);
ALTER TABLE ghost DROP COLUMN type;
