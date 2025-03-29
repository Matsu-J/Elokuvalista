CREATE TABLE app_stats (
    id INTEGER PRIMARY KEY,
    action_type TEXT,
    action_time TEXT
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);