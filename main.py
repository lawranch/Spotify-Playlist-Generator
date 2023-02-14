from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

# ---------------------------- USER INPUT ---------------------------- #
date = input("Which date do you want to make a playlist out of? Type the date in this format YYYY-MM-DD: ")
year = date[0:4]

# ---------------------------- WEB SCRAPING ---------------------------- #
response = requests.get(f"https://billboard.com/charts/hot-100/{date}")
soup = BeautifulSoup(response.text, "html.parser")

titles = soup.select("li ul li h3", class_="c-title")
top_100 = [title.text.strip() for title in titles]

# ---------------------------- SPOTIFY PLAYLIST ---------------------------- #

SPOTIPY_CLIENT_ID = CLIENT_ID
SPOTIPY_CLIENT_SECRET = CLIENT_SECRET
SPOTIPY_REDIRECT_URI = "http://localhost:8888/callback"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope="playlist-modify-private",
        cache_path="token.txt",
        show_dialog=True,
    )
)

user_id = sp.current_user()["id"]

# ---------------------------- SEARCH SPOTIFY SONGS ---------------------------- #
song_uris = []

for song in top_100:
    result = sp.search(q=f"track: {song} year: {year}")

    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"Skipped {song}, doesn't exist in Spotify.")

# ---------------------------- ADD SONGS TO PLAYLIST ---------------------------- #
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
