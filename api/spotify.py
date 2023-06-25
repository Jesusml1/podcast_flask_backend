from flask import Flask, request, url_for, session, redirect, make_response, jsonify
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
load_dotenv()

#traer variables de entorno de render
#client_id = os.environ.get('CLIENT_ID')
#client_secret = os.environ.get('SECRET')
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

app = Flask(__name__)

if __name__ == '__main__':
    app.run()

app.config['SESSION_COOKIE_NAME'] = 'Spotify Cookie'
app.secret_key = 'spotifyappmariiacao'
TOKEN_INFO = 'token_info'

#endpoint para autenticar al usuario y pedir autorizacion
#@app.route("/auth")
#def auth():
    #auth_url = create_spotify_oauth().get_authorize_url()
    #return redirect(auth_url)

def auth():
    return create_spotify_oauth().get_authorize_url()

#endpoint de redireccion despues de recibir autorizacion y que hace la peticion del token
#@app.route("/redirect")
#def redirect_page():
#    session.clear()
#    code = request.args.get('code')
#    token_info = create_spotify_oauth().get_access_token(code)
#    session[TOKEN_INFO] = token_info
#    return redirect(url_for('save_user_info', _external = True))

def request_token(code):
    session.clear()
    token_info = create_spotify_oauth().get_access_token(code)
    session[TOKEN_INFO] = token_info
  
    

#obtener todos los podcast de un usuario
#@app.route("/get-user-podcasts")
#def  get_user_podcasts():
    
#    sp = get_spotify_authorization()
#    podcasts = sp.current_user_saved_shows()

#    response = build_response(podcasts, 200)

#    return response

def get_user_podcasts():
    
    sp = get_spotify_authorization()
    podcasts = sp.current_user_saved_shows()
    response = build_response(podcasts, 200)

    return response



#obtener los episodios de un podcast
#@app.route("/get-episodes-podcast", methods=['POST'])
#def  get_episodes():
#        data = request.get_json()
#        podcast_id  = data.get('id')
#        sp = get_spotify_authorization()
#        episodes = sp.show_episodes(podcast_id)
#        response = build_response(episodes, 200)

#        return response

def  get_episodes_podcast(podcast_id):

    sp = get_spotify_authorization()
    episodes = sp.show_episodes(podcast_id)
    response = build_response(episodes, 200)

    return response

#obtener token y actualizarlo
def get_token():
    token_info = session.get(TOKEN_INFO,None)
    if not token_info:
        redirect(url_for('/auth', external=False))
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if(is_expired):
        spotify_oauth = create_spotify_oauth()
        token_info = spotify_oauth.refresh_access_token(token_info['refresh_token'])

    return token_info


#construir la url autorization de spotify
def create_spotify_oauth():
    return SpotifyOAuth(
        client_id = client_id,
        client_secret = client_secret,
        redirect_uri = url_for('redirect_page', _external= True),
        scope = 'user-read-private user-read-email user-library-read'
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