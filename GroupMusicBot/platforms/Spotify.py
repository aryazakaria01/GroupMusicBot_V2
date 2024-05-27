import re
import config
import spotipy

from config import SPOTIFY_ARTIST_IMG_URL
from spotipy.oauth2 import SpotifyClientCredentials
from youtubesearchpython.__future__ import VideosSearch

class SpotifyAPI:
    def __init__(self):
        self.regex = r"^(https:\/\/open.spotify.com\/)(.*)$"
        self.client_id = config.SPOTIFY_CLIENT_ID
        self.client_secret = config.SPOTIFY_CLIENT_SECRET
        if config.SPOTIFY_CLIENT_ID and config.SPOTIFY_CLIENT_SECRET:
            self.client_credentials_manager = SpotifyClientCredentials(
                self.client_id, self.client_secret
            )
            self.spotify = spotipy.Spotify(
                client_credentials_manager=self.client_credentials_manager
            )
        else:
            self.spotify = None

    async def valid(self, link: str):
        if re.search(self.regex, link):
            return True
        else:
            return False

    async def track(self, link: str):
        # track_id = link.split('/')[-1]
        track = self.spotify.track(link)
        ids = track["id"]
        info = track["name"]
        uri = track["uri"]
        duration = 20
        for artist in track["artists"]:
            fetched = f' {artist["name"]}'
            if "Various Artists" not in fetched:
                info += fetched
        track_details = {
            "title": info,
            "link": uri,
            "vidid": ids,
            "duration_min": duration,
            "thumb": SPOTIFY_ARTIST_IMG_URL,
        }
        # results = VideosSearch(info, limit=1)
        # for result in (await results.next())["result"]:
        #     ytlink = result["link"]
        #     title = result["title"]
        #     vidid = result["id"]
        #     duration_min = result["duration"]
        #     thumbnail = result["thumbnails"][0]["url"].split("?")[0]
        # track_details = {
        #     "title": title,
        #     "link": ytlink,
        #     "vidid": vidid,
        #     "duration_min": duration_min,
        #     "thumb": thumbnail,
        # }
        return track_details, ids

    async def playlist(self, url):
        playlist = self.spotify.playlist(url)
        playlist_id = playlist["id"]
        results = []
        for item in playlist["tracks"]["items"]:
            music_track = item["track"]
            info = music_track["name"]
            for artist in music_track["artists"]:
                fetched = f' {artist["name"]}'
                if "Various Artists" not in fetched:
                    info += fetched
            results.append(info)
        return results, playlist_id

    async def album(self, url):
        album = self.spotify.album(url)
        album_id = album["id"]
        results = []
        for item in album["tracks"]["items"]:
            info = item["name"]
            for artist in item["artists"]:
                fetched = f' {artist["name"]}'
                if "Various Artists" not in fetched:
                    info += fetched
            results.append(info)

        return (
            results,
            album_id,
        )

    async def artist(self, url):
        artistinfo = self.spotify.artist(url)
        artist_id = artistinfo["id"]
        results = []
        artisttoptracks = self.spotify.artist_top_tracks(url)
        for item in artisttoptracks["tracks"]:
            info = item["name"]
            for artist in item["artists"]:
                fetched = f' {artist["name"]}'
                if "Various Artists" not in fetched:
                    info += fetched
            results.append(info)

        return results, artist_id
    
    async def plays(self, url):
        current_playback = self.spotify.current_playback()
        device_id = current_playback['device']['id']
        plays = self.spotify.start_playback(device_id=device_id, uris=[url])

        return plays
