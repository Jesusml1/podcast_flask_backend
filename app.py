from flask import Flask
from api.google_sheets.google_sheets_api import google_sheets_bp

app = Flask(__name__)

app.register_blueprint(google_sheets_bp)

if __name__ == '__main__':
    app.run()