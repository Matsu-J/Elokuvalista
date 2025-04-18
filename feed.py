import db

def all_posts(page, page_size):
    limit = page_size
    offset = page_size*(page-1)
    return db.query("""SELECT p.id, p.user_id, p.title, p.release_year, p.movie_hours, p.movie_minutes, p.rating, p.edited_at, u.id, u.username
                     FROM posts p, users u 
                     WHERE u.id = p.user_id 
                     ORDER BY p.id DESC
                     LIMIT ? OFFSET ?""", [limit, offset])

def newest_first():
    return db.query("""SELECT p.id, p.user_id, p.title, p.release_year, p.movie_hours, p.movie_minutes, p.rating, p.edited_at, u.id, u.username
                     FROM posts p, users u 
                     WHERE u.id = p.user_id
                     AND p.release_year NOT NULL
                     ORDER BY p.release_year DESC""")

def oldest_first():
    return db.query("""SELECT p.id, p.user_id, p.title, p.release_year, p.movie_hours, p.movie_minutes, p.rating, p.edited_at, u.id, u.username
                     FROM posts p, users u 
                     WHERE u.id = p.user_id
                     AND p.release_year NOT NULL
                     ORDER BY p.release_year""")

def longest_first():
    return db.query("""SELECT p.id, p.user_id, p.title, p.release_year, p.movie_hours, p.movie_minutes, p.rating, p.edited_at, u.id, u.username
                     FROM posts p, users u 
                     WHERE u.id = p.user_id
                     AND p.movie_hours NOT NULL
                     AND p.movie_minutes NOT NULL
                     ORDER BY p.movie_hours DESC, p.movie_minutes DESC""")

def shortest_first():
    return db.query("""SELECT p.id, p.user_id, p.title, p.release_year, p.movie_hours, p.movie_minutes, p.rating, p.edited_at, u.id, u.username
                     FROM posts p, users u 
                     WHERE u.id = p.user_id
                     AND p.movie_hours NOT NULL
                     AND p.movie_minutes NOT NULL
                     ORDER BY p.movie_hours, p.movie_minutes""")

def get_post(post_id):
    return db.query("""SELECT p.id, p.user_id, p.title, p.release_year, p.movie_hours, p.movie_minutes, p.rating, p.edited_at, u.id, u.username
                        FROM posts p, users u 
                        WHERE p.id = ? AND p.user_id = u.id""", [post_id])[0]

def search(query):
    return db.query("""SELECT p.id, p.user_id, p.title, p.release_year, p.movie_hours, p.movie_minutes, p.rating, p.edited_at, u.id, u.username
                     FROM posts p, users u 
                     WHERE u.id = p.user_id
                     AND p.title LIKE ?
                     ORDER BY p.id DESC""", [f"%{query}%"])

def count_all():
    return db.query("""SELECT COUNT(title)
                    FROM posts""")[0][0]


def create_post(parameters):
    db.execute("INSERT INTO posts (user_id, title, release_year, movie_hours, movie_minutes, rating, edited_at) VALUES (?, ?, ?, ?, ?, ?, ?)", parameters)

def edit_post(parameters):
    db.execute("UPDATE posts SET title = ?, release_year = ?, movie_hours = ?, movie_minutes = ?, rating = ?, edited_at = ? WHERE id = ?", parameters)

def delete_post(post_id):
    db.execute("DELETE FROM posts WHERE id = ?", [post_id])
