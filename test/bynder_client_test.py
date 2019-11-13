from unittest import mock, TestCase
from bynder_sdk.client.bynder_client import BynderClient
from bynder_sdk.client.asset_bank_client import AssetBankClient
from bynder_sdk.client.collection_client import CollectionClient
from bynder_sdk.client.workflow_client import WorkflowClient
from bynder_sdk.client.pim_client import PIMClient

TOKEN = 'token'


class BynderClientTest(TestCase):
    def setUp(self):
        self.bynder_client = BynderClient(
            domain='test.getbynder.com',
            redirect_uri='https://test.com/',
            client_id='client_id',
            client_secret='client_secret',
            token=TOKEN,
            scopes='offline'
        )

    def test_create_bynder_client(self):
        client = self.bynder_client

        self.assertIsInstance(client.asset_bank_client, AssetBankClient)
        self.assertIsInstance(client.collection_client, CollectionClient)
        self.assertIsInstance(client.pim_client, PIMClient)
        self.assertIsInstance(client.workflow_client, WorkflowClient)

        self.assertEqual(client.session.token, TOKEN)

    @mock.patch('bynder_sdk.oauth2.BynderOAuth2Session')
    def test_fetch_token(self, oauth2_mock):
        client = self.bynder_client
        client.session = oauth2_mock

        kwargs = {
            'code': 'code',
            'timeout': 1,
        }

        client.fetch_token(**kwargs)
        client.session.fetch_token.assert_called_once_with(**kwargs)
