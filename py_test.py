import requests
import webbrowser
from urllib.parse import urlencode, urlparse, parse_qs
#
# # Configuration
client_id = '750128'
client_secret = '81e0f43addb7584c60c1a795d7d14c09934f4d79d7acda7a7f7873ff'
redirect_uri = 'http://auth-client.com:8081/callback/'  # Make sure this matches the registered redirect URI
authorization_endpoint = 'http://auth-server.com:8000/authorize/'
token_endpoint = 'http://auth-server.com:8000/token/'
#
# # Step 1: Redirect the user to the authorization endpoint

# params = {
#     'response_type': 'code',
#     'client_id': client_id,
#     'redirect_uri': redirect_uri,
#     'scope': 'openid profile email profile_image bio',  # Add any additional scopes you need
#     'state': 'ajlfkjdsauio',  # You should use a random string here
# }
#
# url = f'{authorization_endpoint}?{urlencode(params)}'
# print(f'Opening browser for URL: {url}')
# webbrowser.open(url)





# Step 2: User logs in and authorizes the application, then is redirected back to the redirect URI with a code
#
# # # Assuming you have a way to capture the redirected UR

# redirected_url = input('http://auth-client.com:8081/callback/?code=f39bed90155644ac81b1257efd661983&state=ajlfkjdsauio&session_state=ab4fec7f945608a72d97602b263ea2d3719d3897e7ffb6c56ab4d9904ba94175.c4b4be9effda30535a496d857e252113')
# parsed_url = urlparse(redirected_url)
authorization_code = 'caa02cbd4d0e4627a1f7ec256a612fc1'# parse_qs(parsed_url.query).get('code')[0]
state = 'ajlfkjdsauio'# parse_qs(parsed_url.query).get('state')[0]

# Step 3: Exchange the authorization code for an access token
token_data = {
    'grant_type': 'authorization_code',
    'code': authorization_code,
    'redirect_uri': redirect_uri,
    'client_id': client_id,
    'client_secret': client_secret,
}

response = requests.post(token_endpoint, data=token_data)
tokens = response.json()
print(f'Access token response: {tokens}')

access_token = tokens.get('access_token')

id_token = tokens.get('id_token')
refresh_token = tokens.get('refresh_token')

# Optional: Use the access token to make an authenticated request
userinfo_endpoint = 'http://auth-server.com:8000/userinfo/'
headers = {
    'Authorization': f'Bearer {access_token}',
}

userinfo_response = requests.get(userinfo_endpoint, headers=headers)
userinfo = userinfo_response.json()
print(f'User info: {userinfo}')
