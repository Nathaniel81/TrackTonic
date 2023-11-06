import lyricsgenius
import os
from dotenv import load_dotenv

load_dotenv()

genius_access_token = os.getenv('GENIUS_ACCESS_TOKEN')
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')


artist = "Drake"
song_title = "Grammys"

def fetch_lyrics_from_genius(artist, song_title, genius_access_token):
    genius = lyricsgenius.Genius(genius_access_token, timeout=60)
    song = genius.search_song(song_title, artist)
    if song is not None:
        return song.lyrics
    else:
        return None

lyrics = fetch_lyrics_from_genius(artist, song_title, genius_access_token)
if lyrics:
    print(lyrics)
else:
    print("Lyrics not found.")
