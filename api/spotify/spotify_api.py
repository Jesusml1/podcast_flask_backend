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
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

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


#endpoint de redireccion despues de recibir autorizacion y que hace la peticion del token
@spotify_bp.route("/redirect")
def redirect_page():
    session.clear()
    code = request.args.get('code')
    token_info = create_spotify_oauth().get_access_token(code)
    refresh_token = token_info['refresh_token']
    expiration_token = token_info['expires_at']
    access_token = token_info['access_token']

    frontend_redirect_url = f'{frontend_url}?at={access_token}&rt={refresh_token}&t_exp={expiration_token}'
    return redirect(frontend_redirect_url)
    
#obtener todos los podcast de un usuario
@spotify_bp.route("/get-user-podcasts")
def  get_user_podcasts():
    token = request.args.get('token')
    expiration = request.args.get('token_expiration')
    sp = get_spotify_authorization(token, expiration)
    podcasts = sp.current_user_saved_shows()

    response = build_response(podcasts, 200)

    return response

#obtener los episodios de un podcast
@spotify_bp.route("/get-episodes-podcast", methods=['POST'])
def  get_episodes():
        data = request.get_json()
        podcast_id  = data.get('podcast_id')
        token =  data.get('token')
        expiration = data.get('token_expiration')
        sp = get_spotify_authorization(token, expiration)
        episodes = sp.show_episodes(podcast_id)
        response = build_response(episodes, 200)

        return response

@spotify_bp.route("/refresh", methods=['POST'])
def refresh():
    token = request.args.get('refresh_token')
    spotify_oauth = create_spotify_oauth()
    token_info = spotify_oauth.refresh_access_token(token)
    return build_response({'token': token_info['access_token'],'refresh_token': token_info['refresh_token'], 'expiration':token_info['expires_at']}, 200)

def validate_token(token, expiration):
    now = int(time.time())
    is_expired = int(expiration) -now < 60
    if(is_expired):
        return False
    return token

#construir la url autorization de spotify
def create_spotify_oauth():
    return SpotifyOAuth(
        client_id = client_id,
        client_secret = client_secret,
        redirect_uri = url_for('spotify.redirect_page', _external= True),
        scope = scope
    )

def get_spotify_authorization(token, expiration):

    token = validate_token(token, expiration)

    if token == False:
        return build_response({'token_expired':True,'message':'token expirado por favor refresque el token para realizar la solicitud'}, 400)
    
    return spotipy.Spotify(auth=token)

#construir respuestas del endpoint
def build_response(data, status):
    json_response = jsonify(data)
    response = make_response(json_response)
    response.status = status
    return response