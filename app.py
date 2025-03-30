from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import db
import config

app = Flask(__name__)
app.secret_key = config.secret_key()


@app.route("/")
def index():
    return render_template("index.html")
    

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
