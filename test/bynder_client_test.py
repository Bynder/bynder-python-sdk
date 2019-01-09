from unittest import mock, TestCase
from urllib.parse import urljoin
from bynder_sdk.client.bynder_client import BynderClient
from bynder_sdk.client.asset_bank_client import AssetBankClient
from bynder_sdk.client.collection_client import CollectionClient
from bynder_sdk.client.workflow_client import WorkflowClient
from bynder_sdk.client.pim_client import PIMClient


# pylint: disable=too-many-instance-attributes
class BynderClientTest(TestCase):
    """ Test the Bynder client.
    """
    def setUp(self):
        self.api_url = 'https://test.bynder.com'
        self.consumer_key = 'AAAA'
        self.consumer_secret = 'BBBB'
        self.token = 'CCCC'
        self.token_secret = 'DDDD'

        self.bynder_client = BynderClient(
            base_url=self.api_url,
            consumer_key=self.consumer_key,
            consumer_secret=self.consumer_secret,
            token=self.token,
            token_secret=self.token_secret
        )
        self.bynder_client.bynder_request_handler.get = mock.MagicMock()
        self.bynder_client.bynder_request_handler.post = mock.MagicMock()
        self.bynder_client.bynder_request_handler.fetch_token = \
            mock.MagicMock()
        self.bynder_client.credentials.reset = mock.MagicMock()

    def tearDown(self):
        self.bynder_client = None
        self.asset_bank_client = None
        self.collection_client = None

    def test_create_bynder_client(self):
        """ Test if the bynder client is not none.
        """
        self.assertIsInstance(self.bynder_client, BynderClient)

    def test_bynder_client_set_base_url(self):
        """ Test if the bynder client has set the base url
        """
        self.assertIsNotNone(self.bynder_client.base_url)
        self.assertEqual(
            self.bynder_client.base_url,
            self.api_url
        )

    def test_bynder_client_set_credentials(self):
        """ Test if the bynder client has set the credentials
        """
        self.assertIsNotNone(self.bynder_client.credentials)
        self.assertEqual(
            self.bynder_client.credentials.consumer_key,
            self.consumer_key
        )
        self.assertEqual(
            self.bynder_client.credentials.consumer_secret,
            self.consumer_secret
        )
        self.assertEqual(
            self.bynder_client.credentials.token,
            self.token
        )
        self.assertEqual(
            self.bynder_client.credentials.token_secret,
            self.token_secret
        )

    def test_bynder_client_set_request_handler(self):
        """ Test if the bynder client has set the request handler
        """
        self.assertIsNotNone(self.bynder_client.bynder_request_handler)

    def test_get_asset_bank_client(self):
        """ Test if the asset bank client is not none.
        """
        self.assertIsInstance(
            self.bynder_client.asset_bank_client, AssetBankClient)

    def test_get_collection_client(self):
        """ Test if the collection client is not none.
        """
        self.assertIsInstance(
            self.bynder_client.collection_client, CollectionClient)

    def test_get_workflow_client(self):
        """ Test if the workflow client is not none.
        """
        self.assertIsInstance(
            self.bynder_client.workflow_client, WorkflowClient)

    def test_get_pim_client(self):
        """ Test if the PIM client is not none.
        """
        self.assertIsInstance(self.bynder_client.pim_client, PIMClient)

    def test_login(self):
        """ Test if when we call login it will use the correct payload for the
        request and returns successfully.
        """
        credentials = {
            'username': 'johndoe',
            'password': 'admin123'
        }
        self.bynder_client.login(
            credentials.get('username'),
            credentials.get('password')
        )
        self.bynder_client.bynder_request_handler.post.assert_called_with(
            endpoint='/api/v4/users/login/',
            payload=credentials
        )

    def test_authorise_url(self):
        """ Test if when we call authorise url it returns the right url.
        """
        authorise_url_endpoint = (
            '/api/v4/oauth/authorise/?oauth_token={0}').format(
                self.bynder_client.credentials.token
            )
        authorise_url = urljoin(
            self.bynder_client.base_url, authorise_url_endpoint)
        self.assertEqual(
            self.bynder_client.authorise_url(),
            authorise_url
        )

        callback_url = 'https://bynder.com'
        self.assertEqual(
            self.bynder_client.authorise_url(callback_url),
            '{0}&callback={1}'.format(authorise_url, callback_url)
        )

    def test_access_token(self):
        """ Test if when we call access token it will use the correct params for the
        request and returns successfully.
        """
        fetch_token = self.bynder_client.bynder_request_handler.fetch_token
        self.bynder_client.access_token()
        fetch_token.assert_called_with(endpoint='/api/v4/oauth/access_token/')

    def test_request_token(self):
        """ Test if when we call request token it will use the correct params for the
        request and returns successfully.
        """
        fetch_token = self.bynder_client.bynder_request_handler.fetch_token
        self.bynder_client.request_token()
        fetch_token.assert_called_with(endpoint='/api/v4/oauth/request_token/')

    def test_get_derivatives(self):
        """ Test if when we call derivatives it will use the correct params for the
        request and returns successfully.
        """
        self.bynder_client.derivatives()
        self.bynder_client.bynder_request_handler.get.assert_called_with(
            endpoint='/api/v4/derivatives/'
        )

    def test_logout(self):
        """ Test if the reset method in credentials is called on logout.
        """
        self.bynder_client.logout()
        self.bynder_client.credentials.reset.assert_called_with()

    def test_update_tokens(self):
        """ Test if the tokens in the credentials are updated with
        the new tokens.
        """
        new_token = '123ABC'
        new_token_secret = '456DEF'

        self.bynder_client._update_tokens(new_token, new_token_secret)
        self.assertEqual(self.bynder_client.credentials.token, new_token)
        self.assertEqual(
            self.bynder_client.credentials.token_secret, new_token_secret)
