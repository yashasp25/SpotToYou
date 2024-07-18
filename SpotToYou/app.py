from flask import Flask, request, url_for, session, redirect, render_template
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import time
import pandas as pd
from config import client_secret1, client_id1
import subprocess

app = Flask(__name__)
app.secret_key = "hi"
app.config['SESSION_COOKIE_NAME'] = 'Yashas Cookie'
TOKEN_INFO = "token_info"

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=client_id1,
        client_secret=client_secret1,
        redirect_uri=url_for('authorize', _external=True),
        scope="user-library-read"
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/authorize')
def authorize():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')

@app.route('/get_all_tracks')
def get_all_tracks():
    session['token_info'], authorized = get_token()
    session.modified = True
    if not authorized:
        return redirect('/login')
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    results = []
    iter = 0
    while True:
        offset = iter * 50
        iter += 1
        curGroup = sp.current_user_saved_tracks(limit=50, offset=offset)['items']
        for idx, item in enumerate(curGroup):
            track = item['track']
            val = track['name'] + " - " + track['artists'][0]['name']
            results += [val]
        if len(curGroup) < 50:
            break
    
    df = pd.DataFrame(results, columns=["song names"])
    df.to_csv('songs.csv', index=False)
    subprocess.run(["python", "playlist.py"])  # Run playlist.py
    
    return "Playlist created successfully!"

def get_token():
    token_valid = False
    token_info = session.get("token_info", {})

    if not session.get('token_info', False):
        token_valid = False
        return token_info, token_valid

    now = int(time.time())
    is_token_expired = session.get('token_info').get('expires_at') - now < 60

    if is_token_expired:
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(session.get('token_info').get('refresh_token'))

    token_valid = True
    return token_info, token_valid

if __name__ == "__main__":
    app.run(debug=True)
