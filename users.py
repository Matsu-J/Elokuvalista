import db

def create_user(username, hashed_password):
    db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", [username, hashed_password])

def get_user_id(username):
    return db.query("""SELECT id
                    FROM users
                    WHERE username = ?
                    """, [username])[0][0]

def get_password_hash(username):
    return db.query("SELECT password_hash FROM users WHERE username = ?", [username])[0][0]