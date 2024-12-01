import os, pathlib

# Google Auth related constants
GOOGLE_CLIENT_SECRET_FILE_PATH = os.getenv('GOOGLE_CLIENT_SECRET_FILE_PATH')
SCOPES = ['https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile', 'openid']

# General constants
DOMAIN=os.getenv('DOMAIN', 'http://127.0.0.1:8080')
SECRET_KEY=os.getenv('SECRET_KEY')
ALGORITHM=os.getenv('ALGORITHM', 'HS256')