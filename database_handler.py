import db

def all_posts():
    return db.query("""SELECT p.id, p.user_id, p.title, p.release_year, p.movie_hours, p.movie_minutes, p.rating, p.edited_at, u.id, u.username
                     FROM posts p, users u 
                     WHERE u.id = p.user_id 
                     ORDER BY p.id DESC""")

def get_post(post_id):
    return db.query("""SELECT p.id, p.user_id, p.title, p.release_year, p.movie_hours, p.movie_minutes, p.rating, p.edited_at, u.id, u.username
                        FROM posts p, users u 
                        WHERE p.id = ? AND p.user_id = u.id""", [post_id])[0]

def get_user_id(username):
    return db.query("""SELECT id
                    FROM users
                    WHERE username = ?
                    """, [username])[0][0]

def create_post(parameters):
    db.execute("INSERT INTO posts (user_id, title, release_year, movie_hours, movie_minutes, edited_at) VALUES (?, ?, ?, ?, ?, ?)", parameters)

def edit_post(parameters):
    db.execute("UPDATE posts SET title = ?, release_year = ?, movie_hours = ?, movie_minutes = ?, edited_at = ? WHERE id = ?", parameters)