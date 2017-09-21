from urllib.parse import urljoin
from bynder_sdk.oauth.oauth_request_handler import OauthRequestHandler
from bynder_sdk.model.credentials import Credentials
from .asset_bank_client import AssetBankClient
from .collection_client import CollectionClient


class BynderClient:
    """ Client used to login to Bynder and to get an instance of the AssetBankClient.
    """
    # pylint: disable-msg=too-many-arguments
    def __init__(self, base_url, consumer_key, consumer_secret, token=None, token_secret=None):
        self.base_url = base_url
        self._asset_bank_client = None
        self._collection_client = None
        self.credentials = Credentials(
            consumer_key,
            consumer_secret,
            token,
            token_secret
        )
        self.bynder_request_handler = OauthRequestHandler(
            base_url=self.base_url,
            request_credentials=self.credentials
        )

    @property
    def asset_bank_client(self):
        """ Gets an instance of the asset bank client to perform Bynder Asset Bank operations.
        """
        if self._asset_bank_client is None:
            self._asset_bank_client = AssetBankClient(self.bynder_request_handler)
        return self._asset_bank_client

    @property
    def collection_client(self):
        """ Gets an instance of the collection client to perform collection operations.
        """
        if self._collection_client is None:
            self._collection_client = CollectionClient(self.bynder_request_handler)
        return self._collection_client

    def login(self, username, password):
        """ Login using API. To be able to use this method we need to provide an request token
        key/secret with login permissions in settings.ini.
        """
        query = {
            'username': username,
            'password': password
        }
        login_response = self.bynder_request_handler.post(
            endpoint='/api/v4/users/login/',
            payload=query
        )
        self._update_tokens(
            login_response.get('tokenKey', ''),
            login_response.get('tokenSecret', '')
        )
        return login_response

    def request_token(self):
        """ Gets temporary request token pair used to build the authorise URL and login through
        the browser.
        """
        if self.credentials.token or self.credentials.token_secret:
            self.credentials.clear()
            self._update_bynder_request_handler_credentials()
        request_token_response = self.bynder_request_handler.fetch_token(
            endpoint='/api/v4/oauth/request_token/'
        )
        updated_request_tokens = self._update_tokens(
            request_token_response.get('oauth_token')[0],
            request_token_response.get('oauth_token_secret')[0]
        )
        self._update_bynder_request_handler_credentials()
        return updated_request_tokens

    def authorise_url(self, callback_url: str = ''):
        """ Some very valuable information.
        """
        authorise_url_endpoint = '/api/v4/oauth/authorise/?oauth_token={0}'.format(
            self.credentials.token
        )

        if callback_url:
            authorise_url_endpoint = '{0}&callback={1}'.format(authorise_url_endpoint, callback_url)

        return urljoin(self.base_url, authorise_url_endpoint)

    def access_token(self):
        """ Gets temporary access token pair once the user has already accessed the authorise
        URL and logged in through the browser.
        """
        access_token_response = self.bynder_request_handler.fetch_token(
            endpoint='/api/v4/oauth/access_token/'
        )
        updated_access_tokens = self._update_tokens(
            access_token_response.get('oauth_token')[0],
            access_token_response.get('oauth_token_secret')[0]
        )
        self._update_bynder_request_handler_credentials()
        return updated_access_tokens

    def logout(self):
        """ Logout resets your credentials. If the access token key/secret provided in the
        settings have full permission, even after this call, calls to any API endpoint will
        still work.
        """
        self.credentials.reset()
        self._update_bynder_request_handler_credentials()

    def derivatives(self):
        """ Gets the list of the derivatives configured for the current account.
        """
        return self.bynder_request_handler.get(
            endpoint='/api/v4/derivatives/'
        )

    def _update_tokens(self, token, token_secret):
        """ Helper method to update the credentials instance.
        """
        self.credentials.set(token, token_secret)
        return {
            'oauth_token': token,
            'oauth_token_secret': token_secret
        }

    def _update_bynder_request_handler_credentials(self):
        """ Helper method to update the bynder request handler with the latest
        credentials.
        """
        self.bynder_request_handler.credentials = self.credentials
