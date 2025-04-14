import os
from dotenv import load_dotenv
from pathlib import Path


# Point to the .env file in the parent directory
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

GPT_URL = os.getenv("GPT_URL")
GPT_API_VERSION = os.getenv("GPT_API_VERSION")
GPT_ACCESS_TOKEN = os.getenv("GPT_ACCESS_TOKEN")

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URL = os.getenv("SPOTIFY_REDIRECT_URL")
SPOTIFY_BASE_URL = os.getenv("SPOTIFY_BASE_URL")
SPOTIFY_TOKEN_ENDPOINT = os.getenv("SPOTIFY_TOKEN_ENDPOINT")

GENIUS_API_BASE_URL = os.getenv("GENIUS_API_BASE_URL")
GENIUS_CLIENT_ID = os.getenv("GENIUS_CLIENT_ID")
GENIUS_CLIENT_SECRET = os.getenv("GENIUS_CLIENT_SECRET")
GENIUS_ACCESS_TOKEN = os.getenv("GENIUS_ACCESS_TOKEN")
