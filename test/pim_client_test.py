from unittest import mock, TestCase
from bynder_sdk import BynderClient


class PIMClientTest(TestCase):
    """ Test the PIM client.
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
        self.pim_client = self.bynder_client.pim_client
        self.pim_client.bynder_request_handler.get = mock.MagicMock()
        self.pim_client.bynder_request_handler.put = mock.MagicMock()

    def tearDown(self):
        self.bynder_client = None
        self.pim_client = None

    def test_metaproperties(self):
        """ Test if when we call metaproperties it will use the correct params for
        the request and returns successfully.
        """
        self.pim_client.metaproperties()
        self.pim_client.bynder_request_handler.get.assert_called_with(
            endpoint='/api/pim/metaproperties/'
        )

    def test_metaproperty_info(self):
        """ Test if when we call metaproperty info it will use the correct params
        for the request and returns successfully.
        """
        self.pim_client.metaproperty_info(metaproperty_id=1111)
        self.pim_client.bynder_request_handler.get(
            endpoint='/api/pim/metaproperties/{}/'.format(1111)
        )

    def test_metaproperty_options(self):
        """ Test if when we call meteproperty options it will use the correct params
        for the request and returns successfully.
        """
        self.pim_client.metaproperty_options(metaproperty_id=1111)
        self.pim_client.bynder_request_handler.get(
            endpoint='/api/pim/metaproperties/{}/options/'.format(1111)
        )

    def test_edit_metaproperty_option(self):
        """ Test if when we call edit metaproperty option it will use the correct
        params for the request and returns successfully.
        """
        self.pim_client.edit_metaproperty_option(
            metaproperty_option_id=1111,
            children=['2222', '3333']
        )
        self.pim_client.bynder_request_handler.put.assert_called_with(
            endpoint='/api/pim/metapropertyoptions/{}/'.format(1111),
            json={'children': ['2222', '3333']}
        )

        self.pim_client.edit_metaproperty_option(
            metaproperty_option_id='1111',
            children='2222'
        )
        self.pim_client.bynder_request_handler.put.assert_called_with(
            endpoint='/api/pim/metapropertyoptions/{}/'.format(1111),
            json={'children': ['2222']}
        )
