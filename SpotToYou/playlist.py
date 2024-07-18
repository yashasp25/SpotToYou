import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import pandas as pd
from config import client_secrets_file2

# Load the CSV file containing the song names
df = pd.read_csv('songs.csv')
song_titles = df['song names'].tolist()

# Define your YouTube API credentials
api_service_name = "youtube"
api_version = "v3"
client_secrets_file = client_secrets_file2  # Path to your client secret JSON file

# Authenticate with the YouTube API
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
credentials = flow.run_local_server()

youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

# Create a new playlist
request = youtube.playlists().insert(
    part="snippet,status",
    body={
      "snippet": {
        "title": "MyProjectPlaylist",  # Specify the title of your playlist
        "description": "Playlist created by YouTube API"
      },
      "status": {
        "privacyStatus": "private"  # Specify the privacy status of your playlist (private, public, unlisted)
      }
    }
)
response = request.execute()
playlist_id = response['id']

# Search for each song on YouTube and add it to the playlist
for song_title in song_titles:
    request = youtube.search().list(
        part="snippet",
        maxResults=1,
        q=song_title
    )
    response = request.execute()
    if response['items']:
        video_id = response['items'][0]['id']['videoId']
        request = youtube.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlist_id,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": video_id
                    }
                }
            }
        )
        request.execute()
    else:
        print(f"Video for '{song_title}' not found.")

print("Playlist created successfully.")
