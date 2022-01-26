CREATE TABLE IF NOT EXISTS users (
    id BIGINT UNIQUE,
    accessum_id INT
);

CREATE TABLE IF NOT EXISTS accessum_campesters (
    id INT UNIQUE,
    nomen TEXT UNIQUE,
    prioritas INT UNIQUE,
    occasiones TEXT
);

CREATE TABLE IF NOT EXISTS variabilium (
    id INT UNIQUE,
    nomen TEXT UNIQUE,
    genus TEXT,
    valorem TEXT
);

CREATE TABLE IF NOT EXISTS textuum (
    id INT UNIQUE,
    nomen TEXT UNIQUE,
    valorem TEXT
);