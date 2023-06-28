from flask import Flask, request, url_for, session, redirect, make_response, jsonify, Blueprint
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from dotenv import load_dotenv
load_dotenv()
import os


frontend_url = os.getenv('FRONTEND_URL')
scope = 'user-read-private user-read-email playlist-modify-public playlist-read-private'
spotify_bp = Blueprint('spotify', __name__)

#traer variables de entorno de render
#client_id = os.environ.get('CLIENT_ID')
#client_secret = os.environ.get('SECRET')
# client_id = os.getenv('CLIENT_ID')
# client_secret = os.getenv('CLIENT_SECRET')

# app = Flask(__name__)

# app.config['SESSION_COOKIE_NAME'] = 'Spotify Cookie'
# app.secret_key = 'spotifyappmariiacao'
TOKEN_INFO = 'token_info'

#endpoint para autenticar al usuario y pedir autorizacion
@spotify_bp.route("/auth")
def auth():
    auth_url = create_spotify_oauth().get_authorize_url()
    return redirect(auth_url)

@spotify_bp.route("/auth/me")
def me():
    auth_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(auth_manager=auth_manager)
    current_user = sp.current_user()
    return jsonify({"user": current_user})

@spotify_bp.route("/auth/refresh")
def refresh_token():
    # auth_manager = SpotifyClientCredentials()
    # sp = spotipy.Spotify(auth_manager=auth_manager)
    res = SpotifyOAuth.refresh_access_token()
    return jsonify({"res": res})

#endpoint de redireccion despues de recibir autorizacion y que hace la peticion del token
@spotify_bp.route("/redirect")
def redirect_page():
    session.clear()
    code = request.args.get('code')
    token_info = create_spotify_oauth().get_access_token(code)
    session[TOKEN_INFO] = token_info
    refresh_token = token_info['refresh_token']

    frontend_redirect_url = f'{frontend_url}?t={refresh_token}'
    return redirect(frontend_redirect_url )
    # return redirect(url_for('spotify.save_user_info', _external = True))
    
#despues de autorizar redirige a inicio (se puede eliminar)
# @spotify_bp.route("/saveUserInfo")
# def save_user_info():
    
#     return redirect('http://localhost:5173')

#obtener todos los podcast de un usuario
@spotify_bp.route("/get-user-podcasts")
def  get_user_podcasts():
    
    sp = get_spotify_authorization()
    podcasts = sp.current_user_saved_shows()

    response = build_response(podcasts, 200)

    return response

#obtener los episodios de un podcast
@spotify_bp.route("/get-episodes-podcast", methods=['POST'])
def  get_episodes():
        data = request.get_json()
        podcast_id  = data.get('id')
        sp = get_spotify_authorization()
        episodes = sp.show_episodes(podcast_id)
        response = build_response(episodes, 200)

        return response

#obtener token y actualizarlo
def get_token():
    token_info = session.get(TOKEN_INFO,None)
    if not token_info:
        redirect(url_for('login', external=False))
    now = int(time.time())
    is_expired = token_info['expires_at'] -now < 60
    if(is_expired):
        spotify_oauth = create_spotify_oauth()
        token_info = spotify_oauth.refresh_access_token(token_info['refresh_token'])

    return token_info

@spotify_bp.route("/")
def hello_world():
    return "<p>Dashboard</p>"

#construir la url autorization de spotify
def create_spotify_oauth():
    return SpotifyOAuth(
        # client_id = client_id,
        # client_secret = client_secret,
        # redirect_uri = url_for('spotify.redirect_page', _external= True),
        scope = scope
    )

#obtener credenciales de autorizacion de spotify
def get_spotify_authorization():
    try:
        token_info = get_token()
    except:
        return redirect('/auth')
    
    return spotipy.Spotify(auth=token_info["access_token"])

#construir respuestas del endpoint
def build_response(data, status):
    json_response = jsonify(data)
    response = make_response(json_response)
    response.status = status
    return response