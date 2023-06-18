from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session


client_id = 'your_client_id'
client_secret = 'your_client_secret'

client = BackendApplicationClient(client_id=client_id)
oauth = OAuth2Session(client=client)
token_url = 'https://example.com/token'

token = oauth.fetch_token(token_url=token_url, client_id=client_id, client_secret=client_secret)

body = client.prepare_request_body()