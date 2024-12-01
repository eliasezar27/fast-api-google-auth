from decouple import config
import os, pathlib

# Google Auth related constants
GOOGLE_CLIENT_SECRET_FILE = "google_client_secret.json"
SCOPES = ['https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile', 'openid']

# General constants
DOMAIN='http://127.0.0.1:8080'
SECRET_KEY=config('SECRET_KEY')
ALGORITHM='HS256'
MOCK_REDIRECT_LINK='https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=8802760073-2258g3c0m5u1odns22pl6crbodcj3kl2.apps.googleusercontent.com&redirect_uri=http%3A%2F%2F127.0.0.1%3A8080%2Fgoogle%2Fauth%2Foauth2callback&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile&state=KLrxYMlMthuyoxo4GENKWqt4f6rl4O&prompt=consent&access_type=offline'