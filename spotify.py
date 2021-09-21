import requests
import os
from dotenv import find_dotenv, load_dotenv


load_dotenv(find_dotenv())

AUTH_URL = 'https://accounts.spotify.com/api/token'


def get_access_token(client_id, client_secret):

    auth_response = requests.post(AUTH_URL, {
       'grant_type': 'client_credentials',
       'client_id': os.getenv(client_id),
       'client_secret': os.getenv(client_secret),
    })


    auth_response_data = auth_response.json()


    access_token = auth_response_data['access_token']

    return access_token

#https://stmorse.github.io/journal/spotify-api.html

# BASE_URL = 'https://api.spotify.com/v1/browse/new-releases?offset=0&limit=10'



# r = requests.get(BASE_URL, 
#                  headers=headers)
# d = r.json()

# tracktitle = []
# artistname = [] 

# try:
#     for name in d['albums']['items']:
#     #   print(name['name'],'-',name['artists'][0]['name'])
#         tracktitle.append(name['name'])
#         artistname.append(name['artists'][0]['name'])
# except KeyError:
#     print("Couldn't fetch data!")  


def get_top_tracks(token, artist_id):

    BASE_URL = f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks?market=ES'
    
    headers = {
    'Authorization': 'Bearer {token}'.format(token=token)
    }
    
    r = requests.get(BASE_URL, 
                 headers=headers)
    d = r.json()

    tracktitle = []
    trackpic = [] 
    artist_name = d['tracks'][0]['artists'][0]['name']
    song_preview = []

    for track in d['tracks']:
    
      tracktitle.append(track['name'])
      trackpic.append(track['album']['images'][1]['url'])
      song_preview.append(track['preview_url'])
    return tracktitle,trackpic,artist_name,song_preview

