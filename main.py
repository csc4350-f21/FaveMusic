import flask
import os
import spotify
import random

app = flask.Flask(__name__)



@app.route('/')  
def main():
    token = spotify.get_access_token('CLIENT_ID', 'CLIENT_SECRET')
    artist_id = ["06HL4z0CvFAxyc27GXpf02","6qqNVTkY8uBg9cP3Jd7DAH","1McMsnEElThX1knmY4oliG"]

    toptrack = spotify.get_top_tracks(token, random.choice(artist_id))

    tracktitle = toptrack[0]
    trackpic = toptrack[1]
    artist_name = toptrack[2]
    song_preview = toptrack[3]

    return flask.render_template("index.html", len = len(tracktitle), tracktitle=tracktitle, trackpic=trackpic, artist_name=artist_name,song_preview=song_preview)

app.run(
    debug=True
)