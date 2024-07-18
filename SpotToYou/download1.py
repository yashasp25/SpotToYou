from bs4 import BeautifulSoup
from requests_html import HTMLSession
from pathlib import Path
import youtube_dl
import requests
import pandas as pd
import os

def DownloadVideosFromTitles(song_titles):
    ids = []
    for index, item in enumerate(song_titles):
        vid_id = ScrapeVidId(item)
        ids.append(vid_id)
    print("Downloading songs")
    DownloadVideosFromIds(ids)

def DownloadVideosFromIds(video_ids):
    SAVE_PATH = os.path.join(Path.home(), "Downloads/songs")
    try:
        os.mkdir(SAVE_PATH)
    except FileExistsError:
        print("Download folder exists")
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(SAVE_PATH, '%(title)s.%(ext)s'),
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(["https://www.youtube.com/watch?v=" + vid_id for vid_id in video_ids])

def ScrapeVidId(query):
    print("Getting video id for:", query)
    BASIC = "http://www.youtube.com/results?search_query="
    URL = BASIC + query.replace(" ", "+")
    session = HTMLSession()
    response = session.get(URL)
    response.html.render(sleep=1)
    soup = BeautifulSoup(response.html.html, "html.parser")

    results = soup.find('a', id="video-title")
    return results['href'].split('/watch?v=')[1]

def main():
    data = pd.read_csv('songs.csv')
    song_titles = data['song names'].tolist()
    print("Found", len(song_titles), "songs!")
    DownloadVideosFromTitles(song_titles)

if __name__ == "__main__":
    main()
