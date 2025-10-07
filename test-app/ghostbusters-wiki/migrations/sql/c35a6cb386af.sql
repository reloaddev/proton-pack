BEGIN;

CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running upgrade  -> 33018f72f5b1

CREATE TABLE ghost (
    id SERIAL NOT NULL, 
    name VARCHAR(128), 
    PRIMARY KEY (id)
);

INSERT INTO ghost (id, name) VALUES (1, 'Slimer');

INSERT INTO ghost (id, name) VALUES (2, 'Zuul');

INSERT INTO alembic_version (version_num) VALUES ('33018f72f5b1') RETURNING alembic_version.version_num;

-- Running upgrade 33018f72f5b1 -> f3d7dffbf9a3

CREATE TABLE weapon (
    id SERIAL NOT NULL, 
    name VARCHAR(128), 
    PRIMARY KEY (id)
);

INSERT INTO weapon (id, name) VALUES (1, 'Proton Pack');

INSERT INTO weapon (id, name) VALUES (2, 'Slime Blower');

UPDATE alembic_version SET version_num='f3d7dffbf9a3' WHERE alembic_version.version_num = '33018f72f5b1';

-- Running upgrade f3d7dffbf9a3 -> c35a6cb386af

DROP TABLE weapon;

UPDATE alembic_version SET version_num='c35a6cb386af' WHERE alembic_version.version_num = 'f3d7dffbf9a3';

COMMIT;

