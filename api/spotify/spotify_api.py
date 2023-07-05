from flask import Flask, request, url_for, session, redirect, make_response, jsonify, Blueprint
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from dotenv import load_dotenv
load_dotenv()
import os
from api.google_sheets.google_sheets_api import find_user, insert_spotify_data, get_user_id, get_user_token

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

    code = request.args.get('code')
    token_info = create_spotify_oauth().get_access_token(code)
    refresh_token = token_info['refresh_token']
    expiration_token = token_info['expires_at']
    access_token = token_info['access_token']
    token_info = {"access_token":access_token, "expiration_token": expiration_token, "refresh_token": refresh_token}

    sp = get_spotify_authorization(token_info)
    user_info = sp.current_user()
    email_user = user_info["email"]

    is_user_registered = find_user(email_user);
    if is_user_registered == True:
        insert_spotify_data(email_user, access_token, expiration_token, refresh_token)
        user_id = get_user_id(email_user)
        frontend_redirect_url = f'{frontend_url}?user={user_id}'
        return redirect(frontend_redirect_url)
    else:
        return build_response({"error":True, "message": "Usuario no registrado"})
    
#obtener todos los podcast de un usuario
@spotify_bp.route("/get-user-podcasts")
def  get_user_podcasts():
    user_id = request.args.get('id')
    token_info = get_user_token(user_id)

    if(user_id):
        sp = get_spotify_authorization(token_info)
        podcasts = sp.current_user_saved_shows()
        response = build_response(podcasts, 200)
        return response
    else:
        response = build_response({"error":True, "message": "El parámetro id es requerido"}, 400)
        return response

#obtener los episodios de un podcast
@spotify_bp.route("/get-episodes-podcast", methods=['POST'])
def  get_episodes():
        data = request.get_json()
        user_id =  data.get('id')
        podcast_id = data.get('podcast_id')
        
        if(user_id and podcast_id):
            token_info = get_user_token(user_id)
            sp = get_spotify_authorization(token_info)
            episodes = sp.show_episodes(podcast_id)
            response = build_response(episodes, 200)

            return response
        else:
            response = build_response({"error":True, "message": "Los parametros id y podcast_id son requeridos"}, 400)
            return response

#refrescar el token del usuario
def refresh(token_info):
    refresh_token = token_info['refresh_token']
    spotify_oauth = create_spotify_oauth()
    token_info = spotify_oauth.refresh_access_token(refresh_token)
    insert_spotify_data(refresh_token,token_info['access_token'], token_info['expires_at'],token_info['refresh_token'])
    return token_info

#validar expiracion del token
def validate_token(expiration):
    now = int(time.time())
    is_expired = int(expiration) -now < 60
    if(is_expired):
        return False
    return True

#construir la url autorization de spotify
def create_spotify_oauth():
    return SpotifyOAuth(
        client_id = client_id,
        client_secret = client_secret,
        redirect_uri = url_for('spotify.redirect_page', _external= True),
        scope = scope
    )

#obtener la autorizacion de spotify
def get_spotify_authorization(token_info):

    valid_token = validate_token(token_info['expiration_token'])

    if valid_token == False:
        token_info = refresh(token_info)
    
    return spotipy.Spotify(auth=token_info['access_token'])

#construir respuestas del endpoint
def build_response(data, status):
    json_response = jsonify(data)
    response = make_response(json_response)
    response.status = status
    return response