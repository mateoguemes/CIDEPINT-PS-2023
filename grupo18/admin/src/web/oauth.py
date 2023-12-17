from authlib.integrations.flask_client import OAuth
from os import environ

oauth = OAuth()

def init_oauth(app):
    CONF_URL = "https://accounts.google.com/.well-known/openid-configuration"
    oauth.init_app(app)
    oauth.register(
        name="google",
        client_id = environ.get("GOOGLE_CLIENT_ID"),
        client_secret = environ.get("GOOGLE_CLIENT_SECRET"),
        #client_id = "780750903019-3i8g5h149245421pkc1svrbosk0f4qes.apps.googleusercontent.com",
        #client_secret = "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",
        server_metadata_url=CONF_URL,
        client_kwargs={
            "scope": "openid email profile",
            "nonce": False #deshab. la validacion de nonce
        }
    )