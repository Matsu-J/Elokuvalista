from flask import Flask
from flask import redirect, render_template, request, session, abort
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import feed, users, db
import config


app = Flask(__name__)
app.secret_key = config.secret_key()


@app.route("/")
def index():
    posts = feed.all_posts()
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
        users.create_user(username, hashed_password)
    except:
        return "Käyttäjätunnus on jo olemassa" \
        "<br><a href=""/login"">Kirjaudu sisään?</a>"
    
    session["username"] = username
    session["user_id"] = users.get_user_id(username)
    return redirect("/")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/check_login", methods=["POST"])
def check_login():
    username = request.form["username"]
    password = request.form["password"]

    try:
        hashed_password = users.get_password_hash(username)
    except:
        return "Käyttäjätunnusta ei löydy" \
        "<br><a href=""/register"">Rekisteröi uusi käyttäjä</a>"
    
    if check_password_hash(hashed_password, password):
        session["username"] = username
        session["user_id"] = users.get_user_id(username)
        return redirect("/")
    else:
        return "Väärä tunnus tai salasana" \
        "<br><a href=""/login"">Yritä uudelleen</a>"


def require_login():
    if "user_id" not in session:
        abort(403)


@app.route("/logout")
def logout():
    del session["username"]
    del session["user_id"]
    return redirect("/")


@app.route("/add_movie")
def add_movie():
    require_login()
    return render_template("add_movie.html")


@app.route("/create_post", methods=["POST"])
def create_post():
    require_login()
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
    user_id = users.get_user_id(session["username"])

    try:
        feed.create_post([user_id, title, year, hours, minutes, edited_at])
        return "Elokuva lisätty!" \
        "<br><a href=""/"">Palaa etusivulle</a>"
    except:
        return "VIRHE" \
        "<br><a href=""/add_movie"">Yritä uudelleen</a>" \
        "<br><a href=""/"">Palaa etusivulle</a>"


@app.route("/post/<int:post_id>")
def show_post(post_id):
    try:
        post = feed.get_post(post_id)
        return render_template("post.html", post=post)
    except:
        abort(404)


@app.route("/edit_post/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    require_login()
    post = feed.get_post(post_id)
    if post["user_id"] != session["user_id"]:
        abort(403)

    else:
        if request.method == "GET":
            return render_template("edit_post.html", post=post)
        
        if request.method == "POST":
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

            try:
                feed.edit_post([title, year, hours, minutes, edited_at, post_id])
                return "Muokkaukset tallennettu!" \
                "<br><a href=""/"">Palaa etusivulle</a>"
            except:
                return "VIRHE" \
                "<br><a href=""/add_movie"">Yritä uudelleen</a>" \
                "<br><a href=""/"">Palaa etusivulle</a>"


@app.route("/delete_post/<int:post_id>", methods=["GET", "POST"])
def delete_post(post_id):
    require_login()
    try:
        post = feed.get_post(post_id)
    except:
        abort(404)
    if post["user_id"] != session["user_id"]:
        abort(403)
    
    else:
        if request.method == "GET":
            return render_template("delete_post.html", post=post)
        if request.method == "POST":
            if "confirm" in request.form:
                feed.delete_post(post_id)
                return "Elokuva poistettu!" \
                "<br><a href=""/"">Palaa etusivulle</a>"
            return redirect("/post/" + str(post_id))


@app.route("/sorted", methods=["POST"])
def sorted_by_year():
    try:
        sort_by = request.form["sort"]
        if sort_by == "1":
            sorted_by = "Vanhin ensin"
            posts = feed.oldest_first()
        if sort_by == "2":
            sorted_by = "Uusin ensin"
            posts = feed.newest_first()
        if sort_by == "3":
            sorted_by = "Pisin ensin"
            posts = feed.longest_first()
        if sort_by == "4":
            sorted_by = "Lyhyin ensin"
            posts = feed.shortest_first()
        return render_template("sorted.html", posts=posts, sorted_by=sorted_by)
    except:
        return redirect("/")


@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("query")
    results = feed.search(query)
    return render_template("/search.html", posts=results, query=query)