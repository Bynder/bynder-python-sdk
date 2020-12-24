import fnmatch
import os
from unittest import mock, TestCase

from test import create_bynder_client


def _find_file_helper(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result[0]


class UploadClientTest(TestCase):
    """ Test the Upload client.
    """

    def setUp(self):
        self.bynder_client = create_bynder_client()

        self.upload_client = self.bynder_client.upload_client
        self.upload_client.session.get = mock.MagicMock()
        self.upload_client.session.post = mock.MagicMock()
        self.upload_client.file_sha256 = 'random-hex-digest'

    def tearDown(self):
        self.bynder_client = None
        self.asset_bank_client = None

    def test_prepare(self):
        """ Test if when we call _prepare it will use the correct params
        for the
        requests.
        """
        self.upload_client._prepare()
        self.upload_client.session.post.assert_called_with(
            '/v7/file_cmds/upload/prepare'
        )

    def test_upload_chunks(self):
        """ Test if when we call _upload_chunks it will use the correct params
        for the requests. Also test the chunks_count returned.
        """
        file_path = _find_file_helper('test_upload_image.png',
                                      os.getcwd())
        file_id = 1111
        file_data = None
        with open(file_path, "rb") as f:
            file_data = f.read()
        chunks_count, file_size = \
            self.upload_client._upload_chunks(
                file_path, file_id)
        self.assertEqual(chunks_count, 1)
        self.upload_client.session.post.assert_called_with(
            '/v7/file_cmds/upload/{}/chunk/{}'.format(file_id,
                                                      chunks_count - 1),
            data=file_data)

    def test_finalise_file(self):
        """ Test if when we call _finalise_file it will use the correct params
        for the requests.
        """
        file_id = 1111
        file_name = 'image.png'
        file_size = 4000
        chunks_count = 1
        self.upload_client._finalise_file(file_id, file_name, file_size,
                                          chunks_count)
        self.upload_client.session.post.assert_called_with(
            '/v7/file_cmds/upload/{}/finalise_api'.format(file_id),
            data={
                'fileName': file_name,
                'fileSize': file_size,
                'chunksCount': chunks_count,
                'sha256': self.upload_client.file_sha256,
                'intent': 'upload_main_uploader_asset'
            })

    def test_save_media(self):
        """ Test if when we call _save_media it will use the correct params
        for the requests. Test both cases when the media_id is passed and
        when not passed.
        """
        file_id = 1111
        data = {'brandId': "89898989898-89898989-8989"}
        media_id = "5656565656565656569-456"
        self.upload_client._save_media(file_id, data)
        self.upload_client.session.post.assert_called_with(
            '/v4/media/save/{}'.format(file_id), data=data)
        self.upload_client._save_media(file_id, data, media_id)
        self.upload_client.session.post.assert_called_with(
            '/v4/media/{}/save/{}'.format(media_id, file_id), data={})

    def test_save_media_exception(self):
        """ Test if when we call _save_media with an invalid brandId whether
        the exception is raised or not.
        """
        file_id = 1111
        media_id = "5656565656565656569-456"
        with self.assertRaises(Exception):
            self.upload_client._save_media(file_id, {'brandId': ''}, media_id)
