import math
import os
from hashlib import sha256

MAX_CHUNK_SIZE = 1024 * 1024 * 5
MAX_POLLING_ITERATIONS = 60
POLLING_IDLE_TIME = 5


# pylint: disable-msg=too-few-public-methods
class UploadClient():
    """ Client to upload asset to Bynder.
    """

    def __init__(self, session):
        self.session = session

    def upload(self, file_path, media_id, upload_data):
        """
        todo add docs
        :param media_id:
        :param file_path:
        :param upload_data:
        :return:
        """
        try:
            file_name = file_path.rsplit('/', 1)[-1]
            file_id = self._prepare()
            file_sha256 = ''
            with open(file_path, "rb") as f:
                file_sha256 = sha256(f.read()).hexdigest()
            chunks_count, file_size = self._upload_chunks(file_path, file_id)
            correlation_id = self._finalise_file(file_id, file_name, file_size,
                                                 file_sha256, chunks_count)
            media = self._save_media(file_id, upload_data, media_id)
            return {'file_id': file_id, 'correlation_id': correlation_id,
                    'media': media}
        except Exception as ex:
            return {'Message': 'Unable to upload the file.', 'Error': ex}

    def _prepare(self):
        """
        todo add docs
        :return:
        """
        response = self.session.post('/v7/file_cmds/upload/prepare',
                                     is_fs_endpoint=True
                                     )
        file_id = response["file_id"]
        return file_id

    def _read_in_chunks(self, file_object, chunk_size=MAX_CHUNK_SIZE):
        """Lazy function (generator) to read a file piece by piece.
        Default chunk size: MAX_CHUNK_SIZE."""
        while True:
            data = file_object.read(chunk_size)
            if not data:
                break
            yield data

    def _upload_chunks(self, file_path, file_id):
        """
        todo add docs
        :param file_path:
        :param file_id:
        :return:
        """
        chunks_count = 0
        file_size = 0
        with open(file_path, "rb") as f:
            file_size = os.stat(f.fileno()).st_size
            chunks_count = math.ceil(
                file_size / MAX_CHUNK_SIZE)
            chunk_nr = 0
            for chunk in self._read_in_chunks(f):
                self._upload_chunk(file_id, chunk, chunk_nr)
                chunk_nr = chunk_nr + 1

        return chunks_count, file_size

    def _upload_chunk(self, file_id, data, chunk_nr):
        upload_chunk_endpoint = '/v7/file_cmds/upload/{}/chunk/{' \
                                '}'.format(file_id, chunk_nr)
        content_sha256 = {
            'content-sha256': '{}'.format(sha256(data).hexdigest())
        }
        self.session.headers.update(content_sha256)
        self.session.post(
            upload_chunk_endpoint,
            # each chunk sent here
            data=data,
            is_fs_endpoint=True
        )

    def _finalise_file(self, file_id, file_name, file_size, file_sha256,
                       chunks_count):
        # todo complete this doc
        """ Finalises a completely uploaded file.
        """
        finalise_endpoint = '/v7/file_cmds/upload/{}/finalise'.format(
            file_id)

        response = self.session.post(
            finalise_endpoint, need_response_json=False,
            data={
                'fileName': file_name,
                'fileSize': file_size,
                'chunksCount': chunks_count,
                "sha256": file_sha256,
                "intent": "upload_main_uploader_asset",
            },
            is_fs_endpoint=True
        )

        correlation_id = response.headers['x-api-correlation-id']
        return correlation_id

    def _save_media(self, file_id, data, media_id=None):
        """
         todo add docs
        :param file_id:
        :param data:
        :param media_id:
        :return:
        """
        save_endpoint = '/v4/media/save/{}'.format(file_id)
        if media_id:
            save_endpoint = '/v4/media/{}/save/{}'.format(media_id,
                                                          file_id)
            data = {}
        return self.session.post(save_endpoint, data=data)
