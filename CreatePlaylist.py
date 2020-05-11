import json
import os

import google_auth_oauthlib
import googleapiclient
import requests
import youtube_dl

from SpotfiyKeys import spotify_user_id, spotify_token


class CreatePlaylist():

    def __init__(self):
        self.user_id = spotify_user_id
        self.spotify_token = spotify_token
        self.youtube_client = self.get_youtube_client()
        self.all_song_info = {}

    def get_youtube_client(self):
        """ Step1: Login to Youtube"""
        # Copied from the Youtube Data API

        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "YoutubeKeys.json"

        # Get credentials and create an API client
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_console()

        # from the Youtube DATA API
        youtube_client = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        return youtube_client

    def get_like_videos(self):
        """ Step2: Grab your liked videos & Create a dictionary of Important Song Information """

        request = self.youtube_client.videos().list(
            part="snippet,contentDetails,statistics",
            myRating="Like"
        )
        response = request.execute()

        # collect each video and get important information
        for item in response["items"]:
            video_title = item['snippte']['title']
            youtube_url = "https://www.youtube.com/watch?v={}".format(item['id'])

            # use youtube_dl to collect the song name & artist name
            video = youtube_dl.YoutubeDL({}).extract_info(youtube_url, download=False)
            song_name = video['track']
            artist = video['artist']

            # save all important info
            self.all_song_info[video_title] = {
                "youtube_url": youtube_url,
                "song_name": song_name,
                "artist": artist,

                # add url, easy to get the song to put into the playlist
                "sportify_uir": self.get_spotify_uri(song_name, artist)
            }

    def create_playlist(self):
        """ Step3: Create a new playlist"""

        request_body = json.dumps(
            {'name': 'Your Liked Vids',
             "description": 'All Liked Youtube Videos',
             "public": True})

        query = "https://api.spotify.com/v1/users/{}/playlists".format(self.user_id)
        response = requests.post(
            query,
            data=request_body,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer{}".format(spotify_token)
            }
        )

        response_json = response.json()

        # get playlist id
        return response_json['id']

    def get_spotify_uri(self, song_name, artist):
        """ Step4: Search for the song"""

        query = "https://api.spotify.com/v1/search?query=track%3A{}+artist%3A{}&type=track&offset=0&limit=20".format(
            song_name,
            artist
        )

        response = requests.post(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )

        response_json = response.json()
        songs = response_json["tracks"]["items"]

        # only get the first song
        uri = songs[0]["uri"]

        return uri

    def add_song_to_playlist(self):
        """ Step5: Add the song  to the new Spotify playlist"""

        # populate our songs  dictionary
        self.get_like_videos()

        # collect all of uri
        uris = []
        for song, info in self.all_song_info.items():
            uris.append(info["spotify_uri"])

        # create a new playlist
        playlist_id = self.create_playlist()

        # add all songs into the new playlist
        request_data = json.dumps(uris)

        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(playlist_id)

        response = requests.post(
            query,
            data=request_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            })

        response_json = response.json()

        return response_json

