from __future__ import print_function
import os
import json
from flask import make_response, jsonify
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from app.users.model import User, bcrypt

# SCOPES
SCOPES = ["https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/userinfo.profile"]


def get_google_auth_data():
    """
        Collects user profile and verifies email.
    """
    client_config = {
        "installed": {
            "auth_uri": os.getenv("GOOGLE_AUTH_URI"),
            "token_uri": os.getenv("GOOGLE_TOKEN_URI"),
            "redirect_uris": ["http://localhost:7000/"],
            "client_id": os.getenv("GOOGLE_CLIENT_ID"),
            "client_secret": os.getenv("GOOGLE_CLIENT_SECRET")
        }
    }
    os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
    flow = InstalledAppFlow.from_client_config(client_config, scopes=SCOPES)
    credentials = flow.run_local_server(port=0)
    creds = Credentials(
        None,
        refresh_token=credentials.refresh_token,
        token_uri=os.getenv("GOOGLE_TOKEN_URI"),
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET")
    )

    service = build('oauth2', 'v2', credentials=creds)
    user_data = service.userinfo().get().execute()

    # Save user in database
    try:
        user_in_db = User.objects(email=user_data['email']).first()  # check for existence of user
        if not user_in_db:
            User(email=user_data['email'], name=user_data['name'], picture=user_data['picture'],
                 is_verified=user_data['verified_email'],
                 password=bcrypt.generate_password_hash(user_data['id'], 10)).save()
            return {'message': 'successfully signed up user'}
        else:
            return {'message': 'successfully signed in user'}
    except Exception as error:
        print(error)
        return {'error': 'failed to authenticate user'}
