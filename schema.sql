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
    release_year INTEGER DEFAULT NULL,
    movie_hours TEXT DEFAULT NULL,
    movie_minutes TEXT DEFAULT NULL,
    rating TEXT DEFAULT NULL,
    edited_at TEXT
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    post_id INTEGER REFERENCES posts,
    user_id INTEGER REFERENCES users,
    content TEXT,
    rating TEXT DEFAULT NULL,
    edited_at TEXT
);