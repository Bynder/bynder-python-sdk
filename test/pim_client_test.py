from unittest import mock, TestCase

from test import create_bynder_client


class PIMClientTest(TestCase):
    """ Test the PIM client.
    """

    def setUp(self):
        self.bynder_client = create_bynder_client()

        self.pim_client = self.bynder_client.pim_client
        self.pim_client.session.get = mock.MagicMock()
        self.pim_client.session.put = mock.MagicMock()

    def tearDown(self):
        self.bynder_client = None
        self.pim_client = None

    def test_metaproperties(self):
        """ Test if when we call metaproperties it will use the correct
        params for
        the request and returns successfully.
        """
        self.pim_client.metaproperties()
        self.pim_client.session.get.assert_called_with(
            '/pim/metaproperties/'
        )

    def test_metaproperty_info(self):
        """ Test if when we call metaproperty info it will use the correct
        params
        for the request and returns successfully.
        """
        self.pim_client.metaproperty_info(metaproperty_id=1111)
        self.pim_client.session.get(
            f'/pim/metaproperties/{1111}/'
        )

    def test_metaproperty_options(self):
        """ Test if when we call meteproperty options it will use the
        correct params
        for the request and returns successfully.
        """
        self.pim_client.metaproperty_options(metaproperty_id=1111)
        self.pim_client.session.get(
            f'/pim/metaproperties/{1111}/options/'
        )

    def test_edit_metaproperty_option(self):
        """ Test if when we call edit metaproperty option it will use the
        correct
        params for the request and returns successfully.
        """
        self.pim_client.edit_metaproperty_option(
            metaproperty_option_id=1111,
            children=['2222', '3333']
        )
        self.pim_client.session.put.assert_called_with(
            f'/pim/metapropertyoptions/{1111}/',
            json={'children': ['2222', '3333']}
        )

        self.pim_client.edit_metaproperty_option(
            metaproperty_option_id='1111',
            children='2222'
        )
        self.pim_client.session.put.assert_called_with(
            f'/pim/metapropertyoptions/{1111}/',
            json={'children': ['2222']}
        )
