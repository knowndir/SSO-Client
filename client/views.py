import base64
import hashlib
import logging
import secrets

from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseBadRequest
from django.conf import settings
from oauthlib.oauth2 import OAuth2Error
from requests_oauthlib import OAuth2Session
import requests

import os

logger = logging.getLogger(__name__)

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

from .config import (
    OAUTH2_CLIENT_ID, OAUTH2_CLIENT_SECRET, OAUTH2_REDIRECT_URI,
    OAUTH2_AUTHORIZATION_URL, OAUTH2_TOKEN_URL, OAUTH2_USER_INFO_URL, CUSTOM_SCOPES
)

def base64url_encode(input_bytes):
    return base64.urlsafe_b64encode(input_bytes).rstrip(b'=').decode('utf-8')


def generate_code_verifier():
    return base64url_encode(os.urandom(32))


def generate_code_challenge(verifier):
    return base64url_encode(hashlib.sha256(verifier.encode('utf-8')).digest())


def login(request):
    oauth = OAuth2Session(OAUTH2_CLIENT_ID, redirect_uri=OAUTH2_REDIRECT_URI, scope=CUSTOM_SCOPES, )
    code_verifier = secrets.token_urlsafe(128)
    code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode()).digest()).rstrip(b'=').decode(
        'utf-8')

    authorization_url, state = oauth.authorization_url(
        OAUTH2_AUTHORIZATION_URL,
        code_challenge=code_challenge,
        code_challenge_method='S256',
    )

    # Store state and code_verifier in the session
    request.session['oauth_state'] = state
    request.session['code_verifier'] = code_verifier

    print(authorization_url)
    return render(request, 'client/login.html', {
        'authorization_url': authorization_url
    })


def callback(request):
    state = request.GET.get('state')
    code = request.GET.get('code')
    stored_state = request.session.get('oauth_state')
    code_verifier = request.session.get('code_verifier')

    print(f'Code: {code}')
    print(f'stored_state: {stored_state}')
    print(f'code_verifier: {code_verifier}')

    if stored_state is None or code_verifier is None:
        # Handle missing state or code verifier in session
        return render(request, 'error.html',
                      {'message': 'Session state or code verifier is missing. Possible session expiration.'})

    if state != stored_state:
        # Handle state mismatch
        return render(request, 'error.html', {'message': 'State mismatch. Possible CSRF attack.'})

    # Create an OAuth2 session
    oauth = OAuth2Session(OAUTH2_CLIENT_ID, state=state, redirect_uri=OAUTH2_REDIRECT_URI)

    # try:
    # Fetch the token using the authorization code and code verifier
    print(
        f'Fetching token with code: {code}, client_id: {OAUTH2_CLIENT_ID}, client_secret: {OAUTH2_CLIENT_SECRET}, redirect_uri: {OAUTH2_REDIRECT_URI}')
    token = oauth.fetch_token(
        OAUTH2_TOKEN_URL,
        code=code,
        client_id=OAUTH2_CLIENT_ID,
        client_secret=OAUTH2_CLIENT_SECRET,
        code_verifier=code_verifier,
        include_client_id=True,
    )

    # Store the token in the session
    request.session['oauth_token'] = token

    print(token)
    return redirect('profile')


def profile(request):
    oauth = OAuth2Session(OAUTH2_CLIENT_ID, token=request.session['oauth_token'])
    response = oauth.get(OAUTH2_USER_INFO_URL)
    print(response.json())
    print(request.session['oauth_token'])
    user_info = response.json()

    return render(request, 'client/profile.html', {'user_info': user_info})
