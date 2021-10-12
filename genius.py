import requests
import os
from dotenv import find_dotenv, load_dotenv


load_dotenv(find_dotenv())


def lyrics_link(access_token, titletrack, artist_name):

    access_token = os.getenv(access_token)

    base_url = "https://api.genius.com/search/"

    search_data = titletrack + " " + artist_name

    search_input = search_data.replace(" ", "-")

    params = {"q": search_input}

    headers = {
        "Authorization": "Bearer {access_token}".format(access_token=access_token)
    }

    r = requests.get(base_url, params=params, headers=headers)
    d = r.json()
    try:

        return d["response"]["hits"][0]["result"]["url"]

    except KeyError or IndexError:
        return "No lyrics link to be found!"
