"""Spotify"""
import requests
import os
from dotenv import find_dotenv, load_dotenv


load_dotenv(find_dotenv())

AUTH_URL = "https://accounts.spotify.com/api/token"


def get_access_token(client_id, client_secret):
    """Token"""
    auth_response = requests.post(
        AUTH_URL,
        {
            "grant_type": "client_credentials",
            "client_id": os.getenv(client_id),
            "client_secret": os.getenv(client_secret),
        },
    )

    auth_response_data = auth_response.json()

    access_token = auth_response_data["access_token"]

    return access_token


def artist_info(token, artist_id):
    """Info"""
    base_url = f"https://api.spotify.com/v1/artists/{artist_id}"

    headers = {"Authorization": "Bearer {token}".format(token=token)}

    request_data = requests.get(base_url, headers=headers)
    dict_data = request_data.json()

    try:
        artist_name = dict_data["name"]
        return artist_name
    except KeyError:
        return None


def get_top_tracks(token, artist_id):
    """TopTracks"""
    base_url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?market=ES"

    headers = {"Authorization": "Bearer {token}".format(token=token)}

    request_data = requests.get(base_url, headers=headers)
    dict_data = request_data.json()

    tracktitle = []
    trackpic = []
    songpreview = []

    if "error" in dict_data:
        return KeyError

    for track in dict_data["tracks"]:

        tracktitle.append(track["name"])
        trackpic.append(track["album"]["images"][1]["url"])
        songpreview.append(track["preview_url"])

    return (tracktitle, trackpic, songpreview)


def search_id(token, artist_name):
    """Search"""
    search_input = artist_name.replace(" ", "%20")

    base_url = f"https://api.spotify.com/v1/search?q={search_input}&type=artist&market=US&limit=1"

    headers = {"Authorization": "Bearer {token}".format(token=token)}

    request_data = requests.get(base_url, headers=headers)
    try:
        dict_data = request_data.json()
        artist_id = dict_data["artists"]["items"][0]["id"]

        return artist_id
    except IndexError:
        return None
