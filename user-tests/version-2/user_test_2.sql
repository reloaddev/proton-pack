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