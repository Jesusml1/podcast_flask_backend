from flask import Flask
from api.google_sheets.google_sheets_api import google_sheets_bp
from api.spotify.spotify_api import spotify_bp
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.register_blueprint(google_sheets_bp)
app.register_blueprint(spotify_bp)

app.config['SESSION_COOKIE_NAME'] = 'Spotify Cookie'
app.secret_key = 'spotifyappmariiacao'

if __name__ == '__main__':
    app.run()