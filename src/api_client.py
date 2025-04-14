import requests
from pydantic import BaseModel
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URL, GENIUS_API_BASE_URL, GENIUS_ACCESS_TOKEN


SPOTIFY_SCOPE = [
    "user-read-playback-state",
    "user-modify-playback-state",
    "user-read-currently-playing",
    "user-read-private",
    "user-read-email",
    "playlist-read-private",
    "playlist-read-collaborative",
    "playlist-modify-public",
    "playlist-modify-private",
    "user-library-read",
    "user-library-modify",
    "user-top-read",
    "user-read-recently-played",
    "user-follow-read",
    "user-follow-modify",
    "streaming",
    "app-remote-control"
]

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URL,
    scope=" ".join(SPOTIFY_SCOPE)
))


def spotipy_request_impl(function_name: str, **kwargs) -> any:
    try:
        func = getattr(sp, function_name)
        return func(**kwargs)
    except AttributeError:
        raise ValueError(f"Function with name '{function_name}' does not exist.")
    except TypeError as e:
        raise ValueError(f"Invalid parameters for '{function_name}': {str(e)}")


class Song(BaseModel):
    title: str
    artist_names: str


def search_song_by_lyrics_impl(lyrics: str) -> Song | None:
    url = GENIUS_API_BASE_URL
    token = GENIUS_ACCESS_TOKEN

    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "q": lyrics
    }
    response = requests.get(f"{url}/search", headers=headers, params=params)

    if response.status_code == 200:
        results = response.json()["response"]["hits"]

        if len(results) == 0:
            return None
        
        return Song(title=results[0]["result"]["title"], artist_names=results[0]["result"]["artist_names"])
    else:
        raise ValueError(f"API returned error with status code {response.status_code} and message {response.text}")
