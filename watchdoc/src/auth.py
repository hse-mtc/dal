from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from config import (
    WATCHDOC_AUTH_PORT,
    CREDENTIALS_PATH,
    TOKENS_PATH,
    SCOPES,
)


def obtain_credentials():
    creds = None

    if TOKENS_PATH.exists():
        creds = Credentials.from_authorized_user_file(TOKENS_PATH, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH,
                SCOPES,
            )
            creds = flow.run_local_server(
                port=WATCHDOC_AUTH_PORT,
                open_browser=False,
            )

        with open(TOKENS_PATH, "w") as token:
            token.write(creds.to_json())

    return creds
