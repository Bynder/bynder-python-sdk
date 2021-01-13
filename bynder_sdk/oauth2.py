from oauthlib.oauth2 import BackendApplicationClient
from oauthlib.oauth2.rfc6749.errors import (
    MissingTokenError,
    TokenExpiredError,
    OAuth2Error,
)
from requests_oauthlib import OAuth2Session

from bynder_sdk.version import VERSION

UA_HEADER = {
    'User-Agent': 'bynder-python-sdk/{}'.format(VERSION)
}


def api_endpoint_url(session, endpoint):
    if endpoint.startswith('/v6') or endpoint.startswith('/v7'):
        return 'https://{}{}'.format(session.domain, endpoint)
    return 'https://{}/api{}'.format(session.domain, endpoint)


def oauth2_url(domain, endpoint):
    return 'https://{}/v6/authentication/oauth2/{}'.format(domain, endpoint)


class BynderOAuth2Session(OAuth2Session):
    # pylint: disable-msg=too-many-arguments
    def __init__(
        self,
        domain,
        client_id,
        client_secret,
        scope,
        redirect_uri=None,
        token=None,
        token_updater=None,
        **kwargs
    ):
        if not redirect_uri:
            kwargs['client'] = BackendApplicationClient(client_id)
        # Bynder only issues refresh tokens for authorization_code flow
        # and only when offline scope is requested.
        if redirect_uri and 'offline' in scope:
            kwargs['auto_refresh_url'] = oauth2_url(domain, 'token')

        super().__init__(
            client_id=client_id,
            scope=scope,
            redirect_uri=redirect_uri,
            token=token,
            token_updater=token_updater,
            **kwargs)

        self.domain = domain
        self.client_id = client_id
        self.client_secret = client_secret
        self.headers.update(UA_HEADER)

    def authorization_url(self):
        if not self.using_authorization_code:
            raise UserWarning('authorization_url is only used for '
                              'authorization_code grant')
        return super().authorization_url(
            oauth2_url(self.domain, 'auth'),
        )

    def fetch_token(self, code=None, **kwargs):
        if self.using_authorization_code and not code:
            raise ValueError('code is required when using'
                             'authorization_code grant')
        try:
            return super().fetch_token(
                oauth2_url(self.domain, 'token'),
                client_secret=self.client_secret,
                code=code,
                scope=self.scope,
                **kwargs
            )
        except MissingTokenError as exc:
            # The token endpoint currently returns a non spec compliant
            # which can not be interpreted correctly. Reraise with a
            # slightly more descriptive error.
            raise OAuth2Error('Invalid credentials or scope') from exc

    def refresh_token(self, token_url, **kwargs):
        kwargs['auth'] = (self.client_id, self.client_secret)
        return super().refresh_token(token_url, **kwargs)

    def request(self, method, url, *args, **kwargs):
        """ Custom wrapper which provides the following logic for
        requests hitting the API:
         - Update url to include configured domain
         - Raise for exceptions
         - Attempt to parse and return JSON
        """
        if url.startswith('https'):  # Requests from OAuth2Session
            return super().request(method, url, *args, **kwargs)

        # Fetch a token first if not set yet
        if not self.authorized and self.using_client_credentials:
            self.fetch_token()

        url = api_endpoint_url(self, url)
        try:
            response = super().request(method, url, *args, **kwargs)
        except TokenExpiredError:
            if self.using_authorization_code:
                raise

            self.fetch_token()
            response = super().request(method, url, *args, **kwargs)
        response.raise_for_status()

        try:
            return response.json()
        except ValueError:
            return response

    @property
    def using_client_credentials(self):
        return self._client.grant_type == 'client_credentials'

    @property
    def using_authorization_code(self):
        return self._client.grant_type == 'authorization_code'
