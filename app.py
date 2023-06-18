from flask import Flask, jsonify, redirect, request, session
from requests_oauthlib import OAuth2Session
import secrets
import string
import hashlib
import base64

app = Flask(__name__)

if __name__ == 'main':
    app.run(debug=True, port=5000)

@app.route("/")
def dashboard():
    return jsonify({"message": "dashboard"})

app.secret_key = secrets.token_urlsafe(16)
#datos
client_id = 'cdc86d5fd1044af09f8816e0ac9b0787'
client_secret = '28c8b7bcd5ff49699b595ed8ae736fde'
redirect_uri2 = 'http://127.0.0.1:5000/welcome'
scope = 'user-read-private user-read-email'
authorization_base_url = 'https://accounts.spotify.com/authorize'
token_url = 'https://accounts.spotify.com/api/token'
redirect_uri = 'https://localhost:5000/callback'
toke_spotify = ''


@app.route("/login")
def login():
    
    spotify = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=['user-read-private' ,'user-read-email'])
    #code verifier y code challenge
    pkce = create_pkce_verifier_and_challenge()
    session['state'] = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(16))
    authorization_url, _ = spotify.authorization_url(authorization_base_url, code_challenge=pkce['challenge'], code_challenge_method='S256', state=session['state'])
    session['pkce'] = pkce
    return redirect(authorization_url)

    #spotify = OAuth2Session(client_id, redirect_uri=redirect_uri)
    #authorization_url, state = spotify.authorization_url(authorization_base_url)
    #return redirect(authorization_url)
    #return jsonify({"message": "login"})

@app.route('/callback')
def callback():
    spotify = OAuth2Session(client_id, redirect_uri=redirect_uri2, state=session['state'])
    token = spotify.fetch_token(token_url, client_secret=client_secret, authorization_response=request.url, code_verifier=session['pkce']['verifier'])
    token_spotify = 'Token: ' + str(token)
    return toke_spotify

def create_pkce_verifier_and_challenge():
    #creando un code verifier acorde al standar PKCE
    verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).rstrip(b'=').decode('ascii')
    #generate code challenge
    challenge = hashlib.sha256(verifier.encode('ascii')).digest()
    challenge = base64.urlsafe_b64encode(challenge).rstrip(b'=').decode('ascii')
    return {'verifier': verifier, 'challenge': challenge}

@app.route("/upload/<varname>", methods=['POST'])
def uploadPodcast():
    return jsonify({"message": "login"})

@app.route("/welcome")
def welcome():
    return jsonify({"message": "welcome!"})
# @app.route("/")
# def hello_world():
#     return "Hello, World!"