import db

def create_user(username, hashed_password):
    db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", [username, hashed_password])

def get_user_id(username):
    return db.query("""SELECT id
                    FROM users
                    WHERE username = ?
                    """, [username])[0][0]

def get_user(user_id):
    return db.query("""SELECT username
                      FROM users
                      WHERE id = ?""", [user_id])[0][0]

def count_all(user_id):
    return db.query("""SELECT COUNT(title)
                    FROM posts
                    WHERE user_id = ?""", [user_id])[0][0]

def count_ratings(user_id):
    return db.query("""SELECT COUNT(id)
                    FROM posts
                    WHERE user_id = ? 
                    AND rating NOT NULL""", [user_id])[0][0]

def average_rating(user_id):
    return db.query("""SELECT SUM(rating)
                    FROM posts
                    WHERE user_id = ? 
                    AND rating NOT NULL""", [user_id])[0][0]


def get_posts(user_id):
    return db.query("""SELECT p.id, p.user_id, p.title, p.release_year, p.movie_hours, p.movie_minutes, p.rating, p.created_at, p.edited_at, u.id, u.username
                     FROM posts p, users u 
                     WHERE u.id = p.user_id
                     AND p.user_id = ?
                     ORDER BY p.id DESC""", [user_id])

def get_password_hash(username):
    return db.query("SELECT password_hash FROM users WHERE username = ?", [username])[0][0]