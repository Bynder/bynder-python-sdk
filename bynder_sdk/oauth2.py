import random
import string

from requests_oauthlib import OAuth2Session

from bynder_sdk.util import SessionMixin


def oauth2_url(bynder_domain, endpoint):
    return 'https://{}/v6/authentication/oauth2/{}'.format(
        bynder_domain, endpoint)


class BynderOAuth2Session(SessionMixin, OAuth2Session):
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
