from google_auth_oauthlib.flow import Flow
from core.constants.constant import GOOGLE_CLIENT_SECRET_FILE_PATH, SCOPES, DOMAIN


def init_flow():
    return Flow.from_client_secrets_file(
        client_secrets_file=GOOGLE_CLIENT_SECRET_FILE_PATH,
        scopes=SCOPES,
        redirect_uri=f'{DOMAIN}/google/auth/oauth2callback'
    )


