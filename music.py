from flask_login import login_required, current_user
from flask import Blueprint, render_template, redirect, url_for, request, flash
from requests.api import delete
from .models import ArtistID
from . import spotify
import random
from . import genius
from . import db
from sqlalchemy import exc


music = Blueprint("music", __name__)


@music.route("/new")
@login_required
def toptrack():
    idcheck = ArtistID.query.filter_by(user_id=current_user.id).first()

    if idcheck is None:
        return render_template("music.html", idcheck=idcheck)
    else:
        return redirect(url_for("music.user_page"))


get_id = ""


@music.route("/musicadd", methods=["GET", "POST"])
@login_required
def toptrack_post():
    token = spotify.get_access_token("CLIENT_ID", "CLIENT_SECRET")  # spotify token
    get_name = request.form.get("get_name")
    global get_id
    get_id = spotify.search_id(token, get_name)

    # If user enter invalid name or ID
    if get_id == KeyError:
        flash("Invalid name")
        return redirect(url_for("music.toptrack"))

    artist_name = spotify.artist_info(token, get_id)

    new_artist = ArtistID(
        user_id=current_user.id, artistid=get_id, artistname=artist_name
    )

    # add the new aritst id to the database
    db.session.add(new_artist)
    try:
        db.session.commit()
    except exc.SQLAlchemyError:
        flash(artist_name + " already exists. Try something else.")
        return redirect(url_for("music.toptrack"))

    return redirect(url_for("music.user_page"))


@music.route("/musicdelete", methods=["GET", "POST"])
@login_required
def music_delete():

    delete_id = request.form.get("delete_id")
    ArtistID.query.filter_by(artistid=delete_id).delete()
    ArtistID.query.filter_by(artistname=delete_id).delete()
    db.session.commit()

    return redirect(url_for("music.toptrack"))


@music.route("/home")
@login_required
def user_page():
    token = spotify.get_access_token("CLIENT_ID", "CLIENT_SECRET")  # spotify token
    # artist_id = random.choice(
    #     [
    #         "06HL4z0CvFAxyc27GXpf02",
    #         "6qqNVTkY8uBg9cP3Jd7DAH",
    #         "66CXWjxzNUsdJxJ2JdwvnR",
    #         "7n2wHs1TKAczGzO7Dd2rGr",
    #         "163tK9Wjr9P9DmM0AVK7lm",
    #         "6M2wZ9GZgrQXHCFfjv46we",
    #         "0C8ZW7ezQVs4URX5aX7Kqx",
    #         "26VFTg2z8YR0cCuwLzESi2",
    #         "1Xyo4u8uXC1ZmMpatF05PJ",
    #         "5dfZ5uSmzR7VQK0udbAVpf",
    #     ]
    # )  # get random artist id to fetch

    artistid_list = []
    artistname_list = []
    user_data = ArtistID.query.filter_by(user_id=current_user.id).all()
    for data in user_data:
        artistid_list.append(data.artistid)
        artistname_list.append(data.artistname)
    if "get_id" in globals():
        artist_id = get_id
        del globals()["get_id"]
        toptrack = spotify.get_top_tracks(token, artist_id)

        tracktitle = random.choice(
            toptrack[0]
        )  # get random tracktitle from tracktitle list at index 0 from get_top_tracks return values
        index = toptrack[0].index(tracktitle)  # get index of that random track
        trackpic = toptrack[1][
            index
        ]  # get image of that random track at the same index from trackpic list
        artist_name = spotify.artist_info(
            token, artist_id
        )  # get artist's name from artist_info function of spotify.py
        songpreview = toptrack[2][index]  # get song preview link from songpreview list

        lyrics_url = genius.lyrics_link(
            "GENIUS_TOKEN", tracktitle, artist_name
        )  # genius return lyrics link

        return render_template(
            "music.html",
            len=len(artistid_list),
            artistid_list=artistid_list,
            artistname_list=artistname_list,
            tracktitle=tracktitle,
            trackpic=trackpic,
            artist_name=artist_name,
            songpreview=songpreview,
            lyrics_url=lyrics_url,
        )
    else:

        artist_id = random.choice(artistid_list)

        toptrack = spotify.get_top_tracks(token, artist_id)

        tracktitle = random.choice(
            toptrack[0]
        )  # get random tracktitle from tracktitle list at index 0 from get_top_tracks return values
        index = toptrack[0].index(tracktitle)  # get index of that random track
        trackpic = toptrack[1][
            index
        ]  # get image of that random track at the same index from trackpic list
        artist_name = spotify.artist_info(
            token, artist_id
        )  # get artist's name from artist_info function of spotify.py
        songpreview = toptrack[2][index]  # get song preview link from songpreview list

        lyrics_url = genius.lyrics_link(
            "GENIUS_TOKEN", tracktitle, artist_name
        )  # genius return lyrics link

        return render_template(
            "music.html",
            len=len(artistid_list),
            artistid_list=artistid_list,
            artistname_list=artistname_list,
            tracktitle=tracktitle,
            trackpic=trackpic,
            artist_name=artist_name,
            songpreview=songpreview,
            lyrics_url=lyrics_url,
        )
