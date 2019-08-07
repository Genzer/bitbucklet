import json
import os
import click

import requests
from requests.auth import HTTPBasicAuth,  AuthBase
from requests import HTTPError

from bitbucklet.urls import token_url

class AccessToken:
    """Represents an access token obtained from BitBucket Cloud API

    References:
    ====

    https://developer.atlassian.com/cloud/bitbucket/oauth-2/
    """

    def __init__(self, access_token_raw: str):
        self._access_token = json.loads(access_token_raw)

    def token(self):
        return self._access_token['access_token']

    def raw(self):
        return json.dumps(self._access_token)

class BearerAuth(AuthBase):

    def __init__(self, access_token: AccessToken):
        self._access_token = access_token

    def __call__(self, request):
        request.headers['Authorization'] = f"Bearer {self._access_token.token()}"
        return request


def get_access_token():
    """
    Obtains BitBucket AccessToken using the Resource Owner Grant Flow.

    Note:
    ====
    Previously, bitbucklet requires username and password of the account to get
    an Access Token. This was done because the Atlasssian document said so.

    However, this is not the case. Using the `client` and `secret` of the OAuth Consumer
    is enough.

    References:
    ====

    https://developer.atlassian.com/cloud/bitbucket/oauth-2/
    https://bitbucket.org/atlassian/bb-cloud-resource-owner-grant-sample-app/src/master/
    """


    bitbucket_client_id = os.getenv('BITBUCKET_CLIENT_ID')
    bitbucket_client_secret = os.getenv('BITBUCKET_CLIENT_SECRET')

    response = requests.post(
        token_url(),
        auth = HTTPBasicAuth(bitbucket_client_id, bitbucket_client_secret),
        headers = {
            'Accept': 'application/json'
        },
        data = {
            'grant_type': 'client_credentials'
        }
    )

    if response.status_code != 200:
        raise HTTPError(f"Fail to get access token. Payload: \n {response.text}", response=response)

    return AccessToken(response.text)

@click.command(name='tokens', help = 'Tokens')
def token_cli():
    access_token = get_access_token()
    print(access_token.raw())