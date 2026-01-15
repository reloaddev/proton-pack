-- Running upgrade af3c701704d2 -> a9c1d391bad5

ALTER TABLE ghost ALTER COLUMN reporter_id SET NOT NULL DEFAULT -1;

ALTER TABLE ghost ADD FOREIGN KEY(reporter_id) REFERENCES human (id);

CREATE INDEX CONCURRENTLY ON ghost(reporter_id);

UPDATE alembic_version SET version_num='a9c1d391bad5' WHERE alembic_version.version_num = 'af3c701704d2';

COMMIT;

