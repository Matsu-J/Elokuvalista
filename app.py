from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import db
import config


app = Flask(__name__)
app.secret_key = config.secret_key()


@app.route("/")
def index():
    posts = db.query("SELECT * FROM posts p, users u WHERE u.id = p.user_id ORDER BY p.id DESC")
    return render_template("index.html", posts=posts)
    

@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/create_user", methods=["POST"])
def create_user():
    username = request.form["username"]
    password = request.form["password"]
    confirmed_password = request.form["password_confirm"]

    if password != confirmed_password:
        return "Salasanat eivät täsmää!" \
        "<br><a href=""/register"">Yritä uudelleen</a>"
    
    hashed_password = generate_password_hash(password)

    try:
        db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", [username, hashed_password])
    except:
        return "Käyttäjätunnus on jo olemassa" \
        "<br><a href=""/login"">Kirjaudu sisään?</a>"
    
    session["username"] = username
    return redirect("/")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/check_login", methods=["POST"])
def check_login():
    username = request.form["username"]
    password = request.form["password"]

    try:
        hashed_password = db.query("SELECT password_hash FROM users WHERE username = ?", [username])[0][0]
    except:
        return "Käyttäjätunnusta ei löydy" \
        "<br><a href=""/register"">Rekisteröi uusi käyttäjä</a>"
    
    if check_password_hash(hashed_password, password):
        session["username"] = username
        return redirect("/")
    else:
        return "Väärä tunnus tai salasana" \
        "<br><a href=""/login"">Yritä uudelleen</a>"
        

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")


@app.route("/add_movie")
def add_movie():
    return render_template("add_movie.html")


@app.route("/create_post", methods=["POST"])
def create_post():
    title = request.form["title"]
    
    if request.form["release_year"]:
        year = request.form["release_year"]
    else:
        year = None
    
    if request.form["hours"] and request.form["minutes"]:
        hours = request.form["hours"]
        minutes = request.form["minutes"]
    elif request.form["hours"] and not request.form["minutes"]:
        hours = request.form["hours"]
        minutes = 0
    elif not request.form["hours"] and request.form["minutes"]:
        hours = 0
        minutes = request.form["hours"]
    else:
        hours = None
        minutes = None
    
    edited_at = datetime.now()
    user_id = db.query("SELECT id FROM users WHERE username = ?", [session["username"]])[0][0]
    print(user_id)

    try:
        db.execute("INSERT INTO posts (user_id, title, release_year, movie_hours, movie_minutes, edited_at) VALUES (?, ?, ?, ?, ?, ?)", [user_id, title, year, hours, minutes, edited_at])
        return "Elokuva lisätty!" \
        "<br><a href=""/"">Palaa etusivulle</a>"
    except:
        return "VIRHE" \
        "<br><a href=""/add_movie"">Yritä uudelleen</a>" \
        "<br><a href=""/"">Palaa etusivulle</a>"