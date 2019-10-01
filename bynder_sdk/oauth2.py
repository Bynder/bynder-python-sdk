import random
import string

from requests_oauthlib import OAuth2Session


def oauth2_url(bynder_domain, endpoint):
    return 'https://{}/v6/authentication/oauth2/{}'.format(
        bynder_domain, endpoint)


def api_endpoint_url(oauth2_session, endpoint):
    return 'https://{}/api{}'.format(oauth2_session.bynder_domain, endpoint)


def parse_json_for_response(response):
    try:
        return response.json()
    except ValueError:
        return None


class BynderOAuth2Session(OAuth2Session):
    def __init__(self, bynder_domain, *args, **kwargs):
        self.bynder_domain = bynder_domain

        kwargs['auto_refresh_url'] = oauth2_url(self.bynder_domain, 'token')

        super().__init__(*args, **kwargs)

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

        return parse_json_for_response(response)

    def get(self, endpoint, *args, **kwargs):
        return self.wrapped_request(super().get, endpoint, *args, **kwargs)

    def post(self, endpoint, *args, **kwargs):
        if endpoint.startswith('https'):
            return super().post(endpoint, *args, **kwargs)
        return self.wrapped_request(super().post, endpoint, *args, **kwargs)

    def put(self, endpoint, *args, **kwargs):
        return self.wrapped_request(super().put, endpoint, *args, **kwargs)

    def delete(self, endpoint, *args, **kwargs):
        return self.wrapped_request(super().delete, endpoint, *args, **kwargs)
