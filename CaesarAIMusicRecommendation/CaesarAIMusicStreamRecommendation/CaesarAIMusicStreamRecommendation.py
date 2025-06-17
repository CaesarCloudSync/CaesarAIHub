import os
import random
import logging
import ytmusicapi
from typing import List
from dotenv import load_dotenv
from ytmusicapi import YTMusic
from ytmusicapi.auth.oauth.exceptions import UnauthorizedOAuthClient
from models.MusicRecommendation import MusicRecommendations
load_dotenv(".env")
#

class CaesarAIMusicStreamRecommendation:
    def __init__(self,browser=True,oauth=False):        
        # Initialize YTMusic with authentication
        auth_filename = 'browser.json' if browser and not oauth else "oauth.json"
        with open("music_recommendation_headers.txt", "r") as file:
            headers_raw = file.read()
        ytmusicapi.setup(filepath="browser.json", headers_raw=headers_raw)
        self.yt = YTMusic(auth_filename)

    @classmethod
    def setup_oauth(cls):
        cls.CLIENT_ID = os.environ.get("CLIENT_ID","")
        cls.CLIENT_SECRET = os.environ.get("CLIENT_SECRET","")
        ytmusicapi.setup_oauth('oauth.json', client_id=cls.CLIENT_ID, client_secret=cls.CLIENT_SECRET)
        return True
    @classmethod
    def setup_browser(cls,headers_raw:str):
        # Oauth and Browser
        #https://ytmusicapi.readthedocs.io/en/stable/setup/browser.html#copy-authentication-headers
        ytmusicapi.setup(filepath="browser.json", headers_raw=headers_raw)
        return True

    def backup_playlist(self,playlist_name:str,selected_tracks:List[str],description:str="") -> MusicRecommendations:
        new_playlist_id = self.yt.create_playlist(playlist_name,description=description)

        # Add selected tracks to the playlist
        track_ids = [track['videoId'] for track in selected_tracks if track['videoId']]
        if track_ids:
            self.yt.add_playlist_items(new_playlist_id, track_ids)
            logging.info(f"Created playlist '{playlist_name}' with ID: {new_playlist_id}")
        else:
            logging.error("No tracks to add to the playlist.")
    def get_similar_songs(self,song_query:str,playlist_name:str="",max_songs:int=50,description:str="",backup:bool=False,max_search:int=150):

        search_results = self.yt.search(song_query, filter="songs", limit=1)
        if not search_results:
            raise ValueError("No Similar Song Results")

        # Use the first song from search results
        song = search_results[0]
        video_id = song['videoId']
        logging.info(f"Selected song: {song['title']} (videoId: {video_id})")

        # Get initial watch playlist with radio mode and shuffle
        watch_playlist = self.yt.get_watch_playlist(videoId=video_id, radio=True, limit=max_search, shuffle=True)
        tracks = watch_playlist['tracks']
        unique_tracks = {track['videoId']: track for track in tracks}.values()

        # Shuffle and select a random subset of tracks (e.g., up to 50 songs)
        random.shuffle(list(unique_tracks))
        selected_tracks = list(unique_tracks)[:max_songs] # Adjust the number as needed

        # Create a new playlist with a unique name
        if backup: 
            self.backup_playlist(playlist_name,selected_tracks,description)
            
        return MusicRecommendations.model_validate({"music":selected_tracks})

    def get_similiar_songs_from_song_with_seeds(self,song_query:str,playlist_name:str="",max_songs:int=150,description:str="",backup:bool=False,) -> MusicRecommendations:

        search_results = self.yt.search(song_query, filter="songs", limit=1)
        if not search_results:
            raise ValueError("No Similar Song Results")

        # Use the first song from search results
        song = search_results[0]
        video_id = song['videoId']
        logging.info(f"Selected song: {song['title']} (videoId: {video_id})")

        # Get initial watch playlist with radio mode and shuffle
        watch_playlist = self.yt.get_watch_playlist(videoId=video_id, radio=True, limit=round(max_songs * 0.25), shuffle=True)
        tracks = watch_playlist['tracks']
        print(len(tracks))

        # Select a few tracks randomly to use as seeds for additional recommendations
        seed_tracks = random.sample(tracks, min(3, len(tracks)))  # Pick up to 3 tracks
        additional_tracks = []

        # Fetch watch playlists for each seed track
        for seed_track in seed_tracks:
            try:
                seed_video_id = seed_track['videoId']
                new_playlist = self.yt.get_watch_playlist(videoId=seed_video_id, radio=True, limit=round(max_songs * 0.25), shuffle=True)
                additional_tracks.extend(new_playlist['tracks'])
            except Exception as e:
                print(f"Error fetching playlist for seed track {seed_track['title']}: {e}")

        # Combine all tracks and remove duplicates based on videoId
        all_tracks = tracks + additional_tracks
        unique_tracks = {track['videoId']: track for track in all_tracks}.values()

        # Shuffle and select a random subset of tracks (e.g., up to 50 songs)
        random.shuffle(list(unique_tracks))
        selected_tracks = list(unique_tracks) # [:max_songs] # Adjust the number as needed

        # Create a new playlist with a unique name
        if backup: 
            self.backup_playlist(playlist_name,selected_tracks,description)
        return MusicRecommendations.model_validate({"music":selected_tracks})

    def get_similar_songs_from_related_arists(self,song_query,playlist_name="",max_songs=50,description="",backup=False,max_search=150) -> MusicRecommendations:

        search_results = self.yt.search(song_query, filter="songs", limit=5)  # Broader search to get multiple songs
        if not search_results:
            raise ValueError("No Similar Song Results")

        # Pick a random song from search results to introduce variability
        song = search_results[0]# random.choice()
        video_id = song['videoId']
        print(f"Selected song: {song['title']} (videoId: {video_id})")

        # Get artist information to find related artists
        artist_id = song.get('artist', {}).get('artistId')
        related_artists = []
        if artist_id:
            artist_info = self.yt.get_artist(artist_id)
            related_artists = artist_info.get('related', {}).get('browseId', [])

        # Get watch playlist with radio mode and shuffle for the main song
        watch_playlist = self.yt.get_watch_playlist(videoId=video_id, radio=True, limit=max_search, shuffle=True)
        tracks = watch_playlist['tracks']

        # Optionally, get watch playlists for related artists to expand the pool
        for related_artist_id in related_artists[:2]:  # Limit to 2 related artists to avoid rate limits
            try:
                artist_info = self.yt.get_artist(related_artist_id)
                top_song = artist_info.get('songs', {}).get('results', [{}])[0].get('videoId')
                if top_song:
                    related_playlist = self.yt.get_watch_playlist(videoId=top_song, radio=True, limit=max_search, shuffle=True)
                    tracks.extend(related_playlist['tracks'])
            except Exception as e:
                print(f"Error fetching related artist tracks: {e}")

        # Remove duplicates based on videoId
        unique_tracks = {track['videoId']: track for track in tracks}.values()

        # Shuffle and select a random subset of tracks (e.g., up to 50 songs)
        random.shuffle(list(unique_tracks))
        selected_tracks = list(unique_tracks)[:max_songs]  # Adjust the number as needed

        # Create a new playlist with a unique name
        if backup:
            self.backup_playlist(selected_tracks,playlist_name,description)
        return MusicRecommendations.model_validate({"music":selected_tracks})
