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
    movie_hours INTEGER DEFAULT NULL,
    movie_minutes INTEGER DEFAULT NULL,
    rating TEXT DEFAULT NULL,
    created_at TEXT,
    edited_at TEXT DEFAULT NULL
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    post_id INTEGER REFERENCES posts,
    user_id INTEGER REFERENCES users,
    content TEXT,
    rating TEXT DEFAULT NULL,
    created_At TEXT,
    edited_at TEXT DEFAULT NULL
);