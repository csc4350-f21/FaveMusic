"""FAVE APP"""
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import find_dotenv, load_dotenv
from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    request,
    flash,
    Blueprint,
    jsonify,
)
import flask

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import (
    login_user,
    logout_user,
    login_required,
    LoginManager,
    current_user,
)

import spotify
import random
import genius
from sqlalchemy import exc
import json
import sys


load_dotenv(find_dotenv())


app = Flask(__name__, static_folder="./build/static")
# app = Flask(__name__)
# This tells our Flask app to look at the results of `npm build` instead of the
# actual files in /templates when we're looking for the index page file. This allows
# us to load React code into a webpage. Look up create-react-app for more reading on
# why this is necessary.
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
#  Point SQLAlchemy to your Heroku database

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
#   Gets rid of a warning
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_POOL_SIZE"] = 300
app.config["SQLALCHEMY_POOL_TIMEOUT"] = 300

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy(app)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

import models


@login_manager.user_loader
def load_user(user_id):
    """User Loader"""
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return models.User.query.get(user_id)


bp = Blueprint("bp", __name__, template_folder="./build")


@bp.route("/index")
@login_required
def index():
    """Index"""
    # insert the data fetched by your app main page here as a JSON
    nonecheck = models.ArtistID.query.filter_by(user_id=current_user.id).first()
    if nonecheck is None:
        nonecheck = True
        default_data = {
            "nonecheck": nonecheck,
            "username": current_user.name,
        }
        data = json.dumps(default_data)
        return render_template("index.html", data=data,)

    nonecheck = False
    token = spotify.get_access_token("CLIENT_ID", "CLIENT_SECRET")  # spotify token
    artistid_list = []
    artistname_list = []
    for data in models.ArtistID.query.filter_by(user_id=current_user.id).all():
        artistid_list.append(data.artistid.replace("-" + str(current_user.id), ""))
        artistname_list.append(data.artistname)

    artist_id = random.choice(artistid_list)

    title, pic, preview = spotify.get_top_tracks(token, artist_id)

    tracktitle = random.choice(
        title
    )  # get random tracktitle from tracktitle list at index 0 from get_top_tracks return values
    trackpic = pic[
        title.index(tracktitle)
    ]  # get image of that random track at the same index from trackpic list
    artist_name = spotify.artist_info(
        token, artist_id
    )  # get artist's name from artist_info function of spotify.py
    songpreview = preview[
        title.index(tracktitle)
    ]  # get song preview link from songpreview list

    lyrics_url = genius.lyrics_link(
        "GENIUS_TOKEN", tracktitle, artist_name
    )  # genius return lyrics link

    default_data = {
        "nonecheck": nonecheck,
        "username": current_user.name,
        "len": len(artistid_list),
        "artistname_list": artistname_list,
        "tracktitle": tracktitle,
        "trackpic": trackpic,
        "artist_name": artist_name,
        "songpreview": songpreview,
        "lyrics_url": lyrics_url,
    }
    data = json.dumps(default_data)
    return render_template("index.html", data=data)


app.register_blueprint(bp)


@app.route("/login")
def login():
    """Login"""
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_post():
    """Login"""
    email = request.form.get("email")
    password = request.form.get("password")

    user = models.User.query.filter_by(email=email).first()

    # check if the user actually exists
    if not user or not check_password_hash(user.password, password):
        flash("Please check your login details and try again.")
        return redirect(
            url_for("login")
        )  # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user)
    return redirect(url_for("profile"))


@app.route("/signup")
def signup():
    """Signup"""
    return render_template("signup.html")


@app.route("/signup", methods=["POST"])
def signup_post():
    """Signup"""
    email = request.form.get("email")
    name = request.form.get("name")
    password = request.form.get("password")

    user = models.User.query.filter_by(email=email).first()

    if not email or not name or not password:  # for null input
        flash("Information can't be null!")
        return redirect(url_for("signup"))
    if (
        user
    ):  # if a user is found, we want to redirect back to signup page so user can try again
        flash("Email address already exists")
        return redirect(url_for("signup"))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = models.User(
        email=email,
        name=name,
        password=generate_password_hash(password, method="sha256"),
    )

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("login"))


@app.route("/logout")
@login_required
def logout():
    """Logout"""
    logout_user()
    return redirect(url_for("index"))


@app.route("/")
def home():
    """Home"""
    return render_template("main.html")


@app.route("/artistsave", methods=["POST"])
def artistsave():
    """Save"""
    token = spotify.get_access_token("CLIENT_ID", "CLIENT_SECRET")  # spotify token
    combineartistlist = flask.request.json.get("combineartistlist")
    print(combineartistlist, file=sys.stderr)

    db.session.query(models.ArtistID).filter_by(user_id=current_user.id).delete()
    db.session.commit()
    for addname in combineartistlist:
        get_id = spotify.search_id(token, addname)
        if get_id is None:
            continue
        artist_name = spotify.artist_info(token, get_id)

        new_artist = models.ArtistID(
            user_id=current_user.id,
            artistid=get_id + "-" + str(current_user.id),
            artistname=artist_name,
        )
        # add the new aritst id to the database
        db.session.add(new_artist)
        try:
            db.session.commit()
        except exc.SQLAlchemyError:
            continue
    artistname_list = []
    user_data = models.ArtistID.query.filter_by(user_id=current_user.id).all()
    for data in user_data:
        artistname_list.append(data.artistname)

    return jsonify({"finalartistlist": artistname_list})


@app.route("/profile")
@login_required
def profile():
    """Profile"""
    id_count = models.ArtistID.query.filter_by(user_id=current_user.id).count()
    return render_template("profile.html", name=current_user.name, count=id_count)


if __name__ == "__main__":

    app.run(
        host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", 8080)), debug=True
    )
