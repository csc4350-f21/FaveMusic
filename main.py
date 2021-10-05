import flask
import spotify
import random
import genius
import os

app = flask.Flask(__name__)



@app.route('/')  
def main():
    token = spotify.get_access_token('CLIENT_ID', 'CLIENT_SECRET') #spotify token


    artist_id = random.choice(["06HL4z0CvFAxyc27GXpf02","6qqNVTkY8uBg9cP3Jd7DAH","66CXWjxzNUsdJxJ2JdwvnR","7n2wHs1TKAczGzO7Dd2rGr","163tK9Wjr9P9DmM0AVK7lm","6M2wZ9GZgrQXHCFfjv46we","0C8ZW7ezQVs4URX5aX7Kqx","26VFTg2z8YR0cCuwLzESi2","1Xyo4u8uXC1ZmMpatF05PJ","5dfZ5uSmzR7VQK0udbAVpf","2aQnC3DbZB9GbauvhAw7ve"]) #get random artist id to fetch
    

    toptrack = spotify.get_top_tracks(token, artist_id)

    tracktitle = random.choice(toptrack[0]) #get random tracktitle from tracktitle list at index 0 from get_top_tracks return values
    index = toptrack[0].index(tracktitle)   #get index of that random track
    trackpic = toptrack[1][index]           #get image of that random track at the same index from trackpic list
    artist_name = spotify.artist_info(token, artist_id)   #get artist's name from artist_info function of spotify.py
    songpreview = toptrack[2][index]                      #get song preview link from songpreview list 

    lyrics_url = genius.lyrics_link('GENIUS_TOKEN', tracktitle, artist_name)       #genius return lyrics link

    return flask.render_template("index.html", 
                            
                            tracktitle=tracktitle, 
                            trackpic=trackpic, 
                            artist_name=artist_name,
                            songpreview=songpreview,
                            lyrics_url=lyrics_url)

app.run(
    # host='0.0.0.0',
    # port=int(os.getenv("PORT",8080)),
    debug=True
)