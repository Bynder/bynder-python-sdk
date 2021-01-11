import random
import string

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

        super().__init__(*args, **kwargs)

        self._set_ua_header()

    def authorization_url(self):
        state = ''.join([
            random.choice(string.ascii_letters + string.digits)
            for n in range(8)])
        return super().authorization_url(
            oauth2_url(self.bynder_domain, 'auth'),
            state=state
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

    def wrapped_request(self, func, endpoint, *args, **kwargs):
        endpoint = api_endpoint_url(self, endpoint)
        response = func(endpoint, *args, **kwargs)
        response.raise_for_status()
        try:
            return response.json()
        except ValueError:
            return response

    def get(self, url, *args, **kwargs):
        return self.wrapped_request(super().get, url, *args, **kwargs)

    def post(self, url, *args, **kwargs):
        if url.startswith('https'):
            # Do not send the Authorization header to S3
            kwargs['headers'] = {'Authorization': None}
            kwargs['withhold_token'] = True
            return super().post(url, *args, **kwargs)
        return self.wrapped_request(super().post, url, *args, **kwargs)

    def put(self, url, *args, **kwargs):
        return self.wrapped_request(super().put, url, *args, **kwargs)

    def delete(self, url, *args, **kwargs):
        return self.wrapped_request(super().delete, url, *args, **kwargs)

    def _set_ua_header(self):
        self.headers.update(UA_HEADER)
