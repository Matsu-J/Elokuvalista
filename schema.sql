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

CREATE TABLE posts (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    title TEXT,
    movie_hours TEXT DEFAULT NULL,
    movie_minutes TEXT DEFAULT NULL,
    relese_year TEXT DEFAULT NULL,
    rating TEXT DEFAULT NULL,
    edited_at TEXT
);