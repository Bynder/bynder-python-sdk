from unittest import mock, TestCase

from test import create_bynder_client


class AssetBankClientTest(TestCase):
    """ Test the Asset Bank client.
    """

    def setUp(self):
        self.bynder_client = create_bynder_client()

        self.asset_bank_client = self.bynder_client.asset_bank_client
        self.asset_bank_client.session.get = mock.MagicMock()
        self.asset_bank_client.session.post = mock.MagicMock()
        self.asset_bank_client.session.delete = mock.MagicMock()
        self.asset_bank_client.upload_client.upload = mock.MagicMock()

    def tearDown(self):
        self.bynder_client = None
        self.asset_bank_client = None

    def test_brands(self):
        """ Test if when we call brands it will use the correct params for the
        request and returns successfully.
        """
        self.asset_bank_client.brands()
        self.asset_bank_client.session.get.assert_called_with(
            '/v4/brands/'
        )

    def test_tags(self):
        """ Test if when we call tags it will use the correct params for the
        request and returns successfully.
        """
        self.asset_bank_client.tags()
        self.asset_bank_client.session.get.assert_called_with(
            '/v4/tags/',
            params={}
        )

        query = {
            'limit': 10
        }

        self.asset_bank_client.tags(query)
        self.asset_bank_client.session.get.assert_called_with(
            '/v4/tags/',
            params=query
        )

    def test_meta_properties(self):
        """ Test if when we call meta_properties it will use the correct
        params for the
        request and returns successfully.
        """
        self.asset_bank_client.meta_properties()
        self.asset_bank_client.session.get.assert_called_with(
            '/v4/metaproperties/',
            params={}
        )

    def test_media_list(self):
        """ Test if when we call media_list it will use the correct params
        for the
        request and returns successfully.
        """
        self.asset_bank_client.media_list()
        self.asset_bank_client.session.get.assert_called_with(
            '/v4/media/',
            params={}
        )

        query = {
            'count': True,
            'limit': 2,
            'type': 'image',
            'versions': 1
        }

        self.asset_bank_client.media_list(query)
        self.asset_bank_client.session.get.assert_called_with(
            '/v4/media/',
            params=query
        )

    def test_media_info(self):
        """ Test if when we call media_info it will use the correct params
        for the
        request and returns successfully.
        """
        self.asset_bank_client.media_info(media_id=1111)
        self.asset_bank_client.session.get.assert_called_with(
            '/v4/media/1111/',
            params={}
        )

    def test_download_url(self):
        """ Test if when we call download_url it will use the correct params
        for the
        request and returns successfully.
        """
        self.asset_bank_client.media_download_url(media_id=1111)
        self.asset_bank_client.session.get.assert_called_with(
            '/v4/media/1111/download/',
            params={}
        )

    def test_set_media_properties(self):
        """ Test if when we call set_media_properties it will use the
        correct params for the request and returns successfully.
        """
        self.asset_bank_client.set_media_properties(media_id=1111)
        self.asset_bank_client.session.post.assert_called_with(
            '/v4/media/1111/',
            data={}
        )

    def test_delete_media(self):
        """ Test if when we call delete_media it will use the correct params
        for the
        request and returns successfully.
        """
        self.asset_bank_client.delete_media(media_id=1111)
        self.asset_bank_client.session \
            .delete.assert_called_with('/v4/media/1111/')

    def test_create_usage(self):
        """ Test if when we call create_usage it will use the correct params
        for the
        request and returns successfully.
        """
        payload = {
            'integration_id': 2222,
            'asset_id': 1111
        }
        self.asset_bank_client.create_usage(
            integration_id=payload['integration_id'],
            asset_id=payload['asset_id']
        )
        self.asset_bank_client.session.post.assert_called_with(
            '/media/usage/',
            data=payload
        )

    def test_get_usage(self):
        """ Test if when we call get_usage it will use the correct params
        for the
        request and returns successfully.
        """
        self.asset_bank_client.usage()
        self.asset_bank_client.session.get.assert_called_with(
            '/media/usage/', params={}
        )

    def test_delete_usage(self):
        """ Test if when we call delete_usage it will use the correct params
        for the
        request and returns successfully.
        """
        payload = {
            'integration_id': 2222,
            'asset_id': 1111
        }
        self.asset_bank_client.delete_usage(
            integration_id=payload['integration_id'],
            asset_id=payload['asset_id']
        )
        self.asset_bank_client.session \
            .delete.assert_called_with(
            '/media/usage/',
            params=payload
        )

    def test_upload_file(self):
        """ Test if when we call upload_file it will use the correct params
        for the
        requests.
        """
        file_path = 'path_to_a_file.png'
        brand_id = 1111
        self.asset_bank_client.upload_file(
            file_path=file_path, brand_id=brand_id)
        self.asset_bank_client.upload_client.upload.assert_called_with(
            file_path=file_path,
            upload_data={'brandId': brand_id}
        )
