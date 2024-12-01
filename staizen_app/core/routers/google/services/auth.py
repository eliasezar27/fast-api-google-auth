from google_auth_oauthlib.flow import Flow

from core.constants.constant import GOOGLE_CLIENT_SECRET_FILE, SCOPES, DOMAIN


def init_flow():
    return Flow.from_client_secrets_file(
        client_secrets_file=GOOGLE_CLIENT_SECRET_FILE,
        scopes=SCOPES,
        redirect_uri=f'{DOMAIN}/google/auth/oauth2callback'
    )


