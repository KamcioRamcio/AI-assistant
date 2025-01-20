from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def get_credentials():
    creds = None
    if os.path.exists(".auth/token.json"):
        creds = Credentials.from_authorized_user_file(".auth/token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('.auth/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('.auth/token.json', 'w') as token:
            token.write(creds.to_json())

    return creds

