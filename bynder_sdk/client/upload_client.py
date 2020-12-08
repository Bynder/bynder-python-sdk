import math
import os
from hashlib import sha256

MAX_CHUNK_SIZE = 1024 * 1024 * 5
MAX_POLLING_ITERATIONS = 60
POLLING_IDLE_TIME = 5


def _read_in_chunks(file_object, chunk_size=MAX_CHUNK_SIZE):
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: MAX_CHUNK_SIZE."""
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


# pylint: disable-msg=too-few-public-methods
class UploadClient:
    """ Client to upload asset to Bynder.
    """
    file_sha256 = ''

    def __init__(self, session):
        self.session = session

    def upload(self, file_path, media_id, upload_data):
        """Handles the upload of the file.
        :param media_id: The media_id of the asset to be created or updated.
        :param file_path: The path of the asset to be uploaded.
        :param upload_data: The upload_data containing brand_id that can be
        used in the save media endpoint.
        :return: A dict with the keys:
                - file_id: an identifier for the file uploaded
                - correlation_id: The correlation_id of save media request.
                - media: a dict containing save media related info.
        """
        try:
            _, file_name = os.path.split(file_path)
            file_id = self._prepare()
            with open(file_path, "rb") as f:
                self.file_sha256 = sha256(f.read()).hexdigest()
            chunks_count, file_size = self._upload_chunks(file_path, file_id)
            correlation_id = self._finalise_file(file_id, file_name, file_size,
                                                 chunks_count)
            media = self._save_media(file_id, upload_data, media_id)
            return {'file_id': file_id, 'correlation_id': correlation_id,
                    'media': media}
        except Exception as ex:
            return {'Message': 'Unable to upload the file.', 'Error': ex}

    def _prepare(self):
        """Initializes and prepares the file for upload by generating a
        file_id.
        :return: A uuid4 that can be used to identify the file to be uploaded.
        """
        response = self.session.post('/v7/file_cmds/upload/prepare')
        return response["file_id"]

    def _upload_chunks(self, file_path, file_id):
        """Upload the file in chunks of MAX_CHUNK_SIZE.
        :param file_path: The path of the asset to be uploaded.
        :param file_id: The uuid4 used to identify the file to be uploaded.
        :return:
            - chunks_count: The number of chunks in which the file is to
        be uploaded.
            - file_size: The size of the file to be uploaded.
        """
        chunks_count = 0
        file_size = 0
        with open(file_path, "rb") as f:
            file_size = os.stat(f.fileno()).st_size
            chunks_count = math.ceil(
                file_size / MAX_CHUNK_SIZE)
            for chunk_nr, chunk in enumerate(_read_in_chunks(f)):
                self._upload_chunk(file_id, chunk, chunk_nr)

        return chunks_count, file_size

    def _upload_chunk(self, file_id, data, chunk_nr):
        self.session.headers['content-sha256'] = sha256(data).hexdigest()
        self.session.post(
            '/v7/file_cmds/upload/{}/chunk/{}'.format(file_id, chunk_nr),
            data=data
        )

    def _finalise_file(self, file_id, file_name, file_size, chunks_count):
        """Finalises a completely uploaded file.
        :param file_id: The file_id returned from the prepare endpoint.
        :param file_name: The name of the file to be uploaded.
        :param file_size: The size of the file to be uploaded.
        :param chunks_count: The number of chunks in which the file was
        uploaded.
        :return: The correlation_id of save media request.
        """
        response = self.session.post(
            '/v7/file_cmds/upload/{}/finalise_api'.format(file_id),
            data={
                'fileName': file_name,
                'fileSize': file_size,
                'chunksCount': chunks_count,
                "sha256": self.file_sha256,
                "intent": "upload_main_uploader_asset",
            }
        )

        correlation_id = response.headers['x-api-correlation-id']
        return correlation_id

    def _save_media(self, file_id, data, media_id=None):
        """Saves the completely uploaded file.
        :param file_id: The uuid4 used to identify the file to be uploaded.
        :param data: The upload_data containing brand_id.
        :param media_id: The media_id of the asset to be created or updated.
        :return: - success: boolean that indicate the result of the upload
        call.
                - mediaitems: a list of mediaitems created, with at least
                the original.
                - batchId: the batchId of the upload.
                - mediaId: the mediaId update or created.
        """
        save_endpoint = '/v4/media/save/{}'.format(file_id)
        if media_id:
            save_endpoint = '/v4/media/{}/save/{}'.format(media_id,
                                                          file_id)
            data = {}
        return self.session.post(save_endpoint, data=data)
