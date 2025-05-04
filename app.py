from flask import Flask
from flask import redirect, render_template, request, session, abort, flash
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import math, secrets, feed, users, validate, greet, stats, config


app = Flask(__name__)
app.secret_key = config.secret_key()


@app.route("/")
@app.route("/<int:page>")
def index(page=1):
    page_size = 30
    post_count = feed.count_all()
    page_count = math.ceil(post_count/page_size)
    page_count = max(page_count, 1)

    if page < 1:
        return redirect("/1")
    if page > page_count:
        return redirect(f"/{str(page_count)}")

    posts = feed.all_posts(page, page_size)
    greeting = greet.random_greeting()
    stats.action("frontpage")
    return render_template("feed/index.html", 
                           page=page, 
                           page_count=page_count, 
                           posts=posts, 
                           greeting=greeting)
    

def require_login():
    if "user_id" not in session:
        abort(403)


def check_csrf():
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)


@app.route("/register")
def register():
    return render_template("form/register.html")


@app.route("/create_user", methods=["POST"])
def create_user():
    username = request.form["username"]
    password = request.form["password"]
    confirmed_password = request.form["password_confirm"]

    if password != confirmed_password:
        flash("Salasanat eivät täsmää!")
        return redirect("/register")
        
    hashed_password = generate_password_hash(password)

    try:
        users.create_user(username, hashed_password)
    except:
        flash("Käyttäjätunnus on jo olemassa")
        return redirect("/create_user")
    
    session["username"] = username
    session["user_id"] = users.get_user_id(username)
    session["csrf_token"] = secrets.token_hex(16)
    stats.action("create user")
    flash("Käyttäjä luotu!")
    return redirect("/")


@app.route("/login")
def login():
    return render_template("form/login.html")


@app.route("/check_login", methods=["POST"])
def check_login():
    username = request.form["username"]
    password = request.form["password"]

    try:
        hashed_password = users.get_password_hash(username)
    except:
        flash("Käyttäjätunnusta ei löydy")
        return redirect("/login")
    
    if check_password_hash(hashed_password, password):
        session["username"] = username
        session["user_id"] = users.get_user_id(username)
        session["csrf_token"] = secrets.token_hex(16)
        stats.action("login")
        return redirect("/")
    else:
        flash("Tarkista salasana!")
        return redirect("/login")


@app.route("/logout")
def logout():
    del session["username"]
    del session["user_id"]
    del session["csrf_token"]
    return redirect("/")


@app.route("/user/<int:user_id>")
def user_page(user_id):
    try:
        user = (users.get_user(user_id))
    except:
        abort(404)
    
    posts = users.get_posts(user_id)
    average = 0
    if users.average_rating(user_id) and users.count_ratings(user_id) > 0:
        average=(users.average_rating(user_id)/users.count_ratings(user_id))
    return render_template("pages/user.html", 
                           username=user, 
                           user_id=user_id,
                           count_all=users.count_all(user_id),
                           count_ratings=users.count_ratings(user_id),
                           average=average,
                           posts=posts)


@app.route("/add_movie")
def add_movie():
    require_login()
    return render_template("form/add_movie.html")


@app.route("/create_post", methods=["POST"])
def create_post():
    require_login()
    check_csrf()
    title = request.form["title"]

    year = None
    if request.form["release_year"]:
        year = request.form["release_year"]
    
    if request.form["hours"] and request.form["minutes"]:
        hours = request.form["hours"]
        minutes = request.form["minutes"]
    elif request.form["hours"] and not request.form["minutes"]:
        hours = request.form["hours"]
        minutes = 0
    elif not request.form["hours"] and request.form["minutes"]:
        hours = 0
        minutes = request.form["minutes"]
    else:
        hours = None
        minutes = None

    grade = None
    if request.form["grade"]:
        grade = request.form["grade"]
    
    error = validate.check_post_parameters(title, year, hours, minutes, grade)
    if error == None:
        if grade:
            if "," in grade:
                grade = grade.replace(",",".")
            grade = float(grade)
        pass
    else:
        flash(error)
        return redirect("/add_movie")

    edited_at = datetime.now().isoformat(" ", "minutes")
    user_id = users.get_user_id(session["username"])

    try:
        feed.create_post([user_id, title, year, hours, minutes, grade, edited_at])
        stats.action("post created")
        flash("Elokuva lisätty!")
        return redirect("/")
    except:
        flash("VIRHE")
        return redirect("/add_movie")


@app.route("/post/<int:post_id>")
def show_post(post_id):
    try:
        post = feed.get_post(post_id)
        comments = feed.get_comments(post_id)
        return render_template("pages/post.html", post=post, comments=comments)
    except:
        abort(404)


@app.route("/add_comment", methods=["POST"])
def add_comment():
    require_login()
    check_csrf()

    comment = request.form["comment"]

    grade = None
    if request.form["grade"]:
        grade = request.form["grade"]
    
    user_id = session["user_id"]
    post_id = request.form["post_id"]

    error = validate.check_comment(comment, grade, post_id)
    if error == None:
        if grade:
            if "," in grade:
                grade = grade.replace(",",".")
            grade = float(grade)
        edited_at = datetime.now().isoformat(" ", "minutes")
        feed.add_comment(post_id, user_id, comment, grade, edited_at)
        stats.action("comment")
        flash("Kommentti lisätty!")
        return redirect(f"/post/{post_id}")
    else:
        flash(error)
        return redirect(f"/post/{post_id}")


@app.route("/edit_post/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    require_login()
    post = feed.get_post(post_id)
    if post["user_id"] != session["user_id"]:
        abort(403)

    else:
        if request.method == "GET":
            return render_template("form/edit_post.html", post=post)
        
        if request.method == "POST":
            check_csrf()
            title = request.form["title"]

            year = None
            if request.form["release_year"]:
                year = request.form["release_year"]
            
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

            grade = None    
            if request.form["grade"]:
                grade = request.form["grade"]

            error = validate.check_post_parameters(title, year, hours, minutes, grade)
            if error == None:
                if grade:
                    if "," in grade:
                        grade = grade.replace(",",".")
                    grade = float(grade)
                pass
            else:
                flash(error)
                return redirect(f"/edit_post/{post_id}")
                
    
            edited_at = datetime.now().isoformat(" ", "minutes")

            try:
                feed.edit_post([title, year, hours, minutes, grade, edited_at, post_id])
                flash("Muokkaukset tallennettu!") 
                return redirect(f"/post/{post_id}")
            except:
                error = "VIRHE" 
                flash(error)
                return redirect(f"/edit_post/{post_id}")


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
            return render_template("form/delete_post.html", post=post)
        if request.method == "POST":
            check_csrf() 
            if "confirm" in request.form:
                feed.delete_post(post_id)
                flash("Elokuva poistettu!")
                return redirect("/")
            return redirect(f"/post/{post_id}")


@app.route("/sorted", methods=["POST"])
def sorted():
    greeting = greet.random_greeting()
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
        return render_template("feed/sorted.html", posts=posts, sorted_by=sorted_by, greeting=greeting)
    except:
        return redirect("/")


@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("query")
    results = feed.search(query)
    greeting = greet.random_greeting()
    return render_template("feed/search.html", posts=results, query=query, greeting=greeting)