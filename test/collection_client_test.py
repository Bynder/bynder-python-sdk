import json
from unittest import mock, TestCase

from test import create_bynder_client


class CollectionClientTest(TestCase):
    """ Test the collection client.
    """

    def setUp(self):
        self.bynder_client = create_bynder_client()

        self.collection_client = self.bynder_client.collection_client
        self.collection_client.session.get = mock.MagicMock()
        self.collection_client.session.post = mock.MagicMock()
        self.collection_client.session.delete = mock.MagicMock()

    def tearDown(self):
        self.bynder_client = None
        self.collection_client = None

    def test_collections(self):
        """ Test if when we call collections it will use the correct params
        for the
        request and returns successfully.
        """
        self.collection_client.collections()
        self.collection_client.session.get.assert_called_with(
            '/v4/collections/',
            params={}
        )

    def test_collection_info(self):
        """ Test if when we call collection info it will use the correct
        params for the
        request and returns successfully.
        """
        self.collection_client.collection_info(collection_id=1111)
        self.collection_client.session.get.assert_called_with(
            '/v4/collections/1111/'
        )

    def test_create_collection(self):
        """ Test if when we call create collections it will use the correct
        params for the request and returns successfully.
        """
        collection_name = 'Unit Test'
        self.collection_client.create_collection(
            name=collection_name
        )
        self.collection_client.session.post.assert_called_with(
            '/v4/collections/',
            data={'name': collection_name}
        )

    def test_delete_collection(self):
        """ Test if when we call delete collections it will use the correct
        params for the request and returns successfully.
        """
        self.collection_client.delete_collection(collection_id=1111)
        self.collection_client.session.delete \
            .assert_called_with('/v4/collections/1111/')

    def test_collection_media_ids(self):
        """ Test if when we call collection media ids it will use the correct
        params for the request and returns successfully.
        """
        self.collection_client.collection_media_ids(collection_id=1111)
        self.collection_client.session.get.assert_called_with(
            '/v4/collections/1111/media/'
        )

    def test_add_media_to_collection(self):
        """ Test if when we call add media to collection it will use the
        correct
        params for the request and returns successfully.
        """
        media_ids = ['2222', '3333']
        self.collection_client.add_media_to_collection(
            collection_id=1111, media_ids=media_ids)
        self.collection_client.session.post.assert_called_with(
            '/v4/collections/1111/media/',
            data={'data': json.dumps(media_ids)}
        )

    def test_remove_media_from_collection(self):
        """ Test if when we call remove media from collection it will use
        the correct
        params for the request and returns successfully.
        """
        media_ids = ['2222', '3333']
        self.collection_client.remove_media_from_collection(
            collection_id=1111, media_ids=media_ids)
        self.collection_client.session \
            .delete \
            .assert_called_with('/v4/collections/1111/media/',
                                params={'deleteIds': ','.join(map(str,
                                                                  media_ids))})

    def test_share_collection(self):
        """ Test if when we call share collection it will use the correct
        params for the request and returns successfully.
        """
        self.collection_client.share_collection(
            collection_id=1111,
            collection_option='view',
            recipients=[]
        )
        self.collection_client.session.post.assert_called_with(
            '/v4/collections/1111/share/',
            data={
                'collectionOptions': 'view',
                'recipients': ','.join(map(str, []))
            }
        )
