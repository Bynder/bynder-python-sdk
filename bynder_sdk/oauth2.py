from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

from bynder_sdk.version import VERSION

UA_HEADER = {
    'User-Agent': 'bynder-python-sdk/{}'.format(VERSION)
}


def api_endpoint_url(session, endpoint):
    if endpoint.startswith('/v6') or endpoint.startswith('/v7'):
        return 'https://{}{}'.format(session.bynder_domain, endpoint)
    return 'https://{}/api{}'.format(session.bynder_domain, endpoint)


def oauth2_url(bynder_domain, endpoint):
    return 'https://{}/v6/authentication/oauth2/{}'.format(
        bynder_domain, endpoint)


class BynderOAuth2Session(OAuth2Session):
    def __init__(self, bynder_domain, *args, **kwargs):
        self.bynder_domain = bynder_domain

        kwargs['auto_refresh_url'] = oauth2_url(self.bynder_domain, 'token')

        if kwargs['redirect_uri'] is None:
            kwargs['client'] = BackendApplicationClient(client_id=kwargs['client_id'])

        super().__init__(*args, **kwargs)

        self.headers.update(UA_HEADER)

    def authorization_url(self):
        return super().authorization_url(
            oauth2_url(self.bynder_domain, 'auth'),
        )

    def fetch_token(self, code, *args, **kwargs):
        return super().fetch_token(
            oauth2_url(self.bynder_domain, 'token'),
            client_secret=self.auto_refresh_kwargs['client_secret'],
            include_client_id=True,
            code=code,
            *args,
            **kwargs
        )

    def request(self, method, url, *args, **kwargs):
        """ Custom wrapper which provides the following logic for
        requests hitting the API:
         - Update url to include configured domain
         - Raise for exceptions
         - Attempt to parse and return JSON
        """
        if url.startswith('https'):  # Requests from OAuth2Session
            return super().request(method, url, *args, **kwargs)

        url = api_endpoint_url(self, url)
        response = super().request(method, url, *args, **kwargs)
        response.raise_for_status()

        try:
            return response.json()
        except ValueError:
            return response
