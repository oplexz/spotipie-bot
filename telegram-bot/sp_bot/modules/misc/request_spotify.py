import logging
import requests
import json
from sp_bot import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI


class InvalidGrantError(Exception):
    """Raised when Spotify returns "invalid_grant" error"""
    pass


class SpotifyUser:
    authorize_url = "https://accounts.spotify.com/authorize"
    token_url = "https://accounts.spotify.com/api/token"

    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    def getAuthUrl(self):
        authorization_redirect_url = self.authorize_url + '?response_type=code&client_id=' + \
            self.client_id + '&redirect_uri=' + self.redirect_uri + \
            '&scope=user-read-currently-playing'
        return authorization_redirect_url

    def getAccessToken(self, authCode: str):
        data = {'grant_type': 'authorization_code',
                'code': authCode, 'redirect_uri': self.redirect_uri}
        r = requests.post(
            self.token_url, data=data, allow_redirects=True, auth=(self.client_id, self.client_secret))

        if r.status_code in range(200, 299):
            res = json.loads(r.text)
            return res['refresh_token']
        else:
            return 'error'

    def getCurrentlyPlayingSong(self, refreshToken: str):
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': refreshToken,
            'redirect_uri': self.redirect_uri,
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }

        try:
            token = requests.post(self.token_url, data=data).json()
            if 'error' in token:
                if token['error'] == 'invalid_grant':
                    raise InvalidGrantError(token['error_description'])
                else:
                    raise ValueError(
                        f"{token['error']}: {token['error_description']}")

            if 'access_token' in token:
                headers = {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + token['access_token']
                }
                r = requests.get(
                    'https://api.spotify.com/v1/me/player/currently-playing', headers=headers)
                r.raise_for_status()
                return r
            else:
                raise ValueError('access_token is not defined')
        except InvalidGrantError:
            raise
        except:
            logging.exception(
                "Something went wrong while making a request to Spotify API. Try ")
            return None


SPOTIFY = SpotifyUser(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
