const axios = require('axios');
const open = require('open');
const readline = require('readline-sync');
const querystring = require('querystring');

// Configuration
const clientId = 'your_client_id';
const clientSecret = 'your_client_secret';
const redirectUri = 'http://localhost:8000/callback'; // Make sure this matches the registered redirect URI
const authorizationEndpoint = 'http://auth-server/authorize';
const tokenEndpoint = 'http://auth-server/token';
const userinfoEndpoint = 'http://auth-server/userinfo';

// Step 1: Redirect the user to the authorization endpoint
const params = {
    response_type: 'code',
    client_id: clientId,
    redirect_uri: redirectUri,
    scope: 'openid profile email', // Add any additional scopes you need
    state: 'random_state_string' // You should use a random string here
};

const authorizationUrl = `${authorizationEndpoint}?${querystring.stringify(params)}`;
console.log(`Opening browser for URL: ${authorizationUrl}`);
open(authorizationUrl);

// Step 2: User logs in and authorizes the application, then is redirected back to the redirect URI with a code
const redirectedUrl = readline.question('Paste the full redirect URL here: ');
const urlParams = new URLSearchParams(redirectedUrl.split('?')[1]);
const authorizationCode = urlParams.get('code');
const state = urlParams.get('state');

// Step 3: Exchange the authorization code for an access token
const tokenData = {
    grant_type: 'authorization_code',
    code: authorizationCode,
    redirect_uri: redirectUri,
    client_id: clientId,
    client_secret: clientSecret
};

axios.post(tokenEndpoint, querystring.stringify(tokenData))
    .then(response => {
        const tokens = response.data;
        console.log('Access token response:', tokens);

        const accessToken = tokens.access_token;
        const idToken = tokens.id_token;
        const refreshToken = tokens.refresh_token;

        // Optional: Use the access token to make an authenticated request
        const headers = {
            'Authorization': `Bearer ${accessToken}`
        };

        return axios.get(userinfoEndpoint, { headers });
    })
    .then(userinfoResponse => {
        const userinfo = userinfoResponse.data;
        console.log('User info:', userinfo);
    })
    .catch(error => {
        console.error('Error:', error.response ? error.response.data : error.message);
    });
