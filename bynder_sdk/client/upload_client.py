import os
import time


MAX_CHUNK_SIZE = 1024 * 1024 * 5
MAX_POLLING_ITERATIONS = 60
POLLING_IDLE_TIME = 10


# pylint: disable-msg=too-few-public-methods
class UploadClient():
    """ Client to upload asset to Bynder.
    """
    def __init__(self, session):
        self.session = session

    @staticmethod
    def _retrieve_filename(file_path):
        return file_path.rsplit('/', 1)[-1]

    def upload(self, file_path, media_id, upload_data):
        """ Handles the upload of the file.
        """
        init_data, total_parts = self._run_s3_upload(file_path)
        finalise_data = self._finalise_file(init_data, total_parts)
        return self._save_media(finalise_data['importId'],
                                upload_data, media_id)

    @staticmethod
    def _update_multipart(filename, total_parts, init_data, part_nr):
        key = init_data['multipart_params']['key']
        init_data['multipart_params'].update({
            'name': filename,
            'chunk': part_nr,
            'chunks': total_parts,
            'Filename': key
        })
        return init_data

    def _run_s3_upload(self, file_path):
        """ Uploads the media to Amazon S3 bucket-endpoint.
        """
        filename = self._retrieve_filename(file_path)
        init_data = self._init_upload(filename)
        with open(file_path, 'rb') as f:
            part_nr = 0
            total_parts = (os.fstat(f.fileno()).st_size + MAX_CHUNK_SIZE - 1)\
                // MAX_CHUNK_SIZE

            part_bytes = f.read(MAX_CHUNK_SIZE)
            while part_bytes:
                part_nr = part_nr + 1
                init_data = self._update_init_data(init_data, part_nr)
                init_data = self._update_multipart(filename, total_parts,
                                                   init_data, part_nr)
                response = self.session.post(
                    self.upload_url,
                    files={"file": part_bytes},
                    data=init_data['multipart_params'],
                    withhold_token=True,
                )
                response.raise_for_status()
                self._register_part(init_data, part_nr)
                part_bytes = f.read(MAX_CHUNK_SIZE)
        return init_data, total_parts

    def _init_upload(self, filename):
        """ Gets the URL of the Amazon S3 bucket-endpoint in the region
        closest to the server and initialises a file upload with Bynder
        and returns authorisation information to allow uploading to the
        Amazon S3 bucket-endpoint.
        """
        self.upload_url = self.session.get('/upload/endpoint/')

        payload = {'filename': filename}
        return self.session.post(
            '/upload/init/',
            data=payload
        )

    @staticmethod
    def _update_init_data(init_data, part_nr):
        """ Updates the init data.
        """
        key = '{}/p{}'.format(
            init_data['s3_filename'],
            part_nr
        )
        init_data['s3_filename'] = key
        init_data['multipart_params']['key'] = key
        return init_data

    def _register_part(self, init_data, part_nr):
        """ Registers an uploaded chunk in Bynder.
        """
        self.session.post(
            '/v4/upload/',
            data={
                'id': init_data['s3file']['uploadid'],
                'targetid': init_data['s3file']['targetid'],
                'filename': init_data['s3_filename'],
                'chunkNumber': part_nr
            }
        )

    def _finalise_file(self, init_data, total_parts):
        """ Finalises a completely uploaded file.
        """
        return self.session.post(
            '/v4/upload/{0}/'.format(
                init_data['s3file']['uploadid']),
            data={
                'id': init_data['s3file']['uploadid'],
                'targetid': init_data['s3file']['targetid'],
                's3_filename': init_data['s3_filename'],
                'chunks': total_parts
            }
        )

    def _save_media(self, import_id, data, media_id=None):
        """ Saves a new media asset in Bynder. If media id is specified
        in the query a new version of the asset will be saved. Otherwise
        a new asset will be saved.
        """
        poll_status = self._poll_status(import_id)
        if import_id not in poll_status['itemsDone']:
            raise Exception("Converting media failed")

        save_endpoint = '/v4/media/save/{}/'.format(import_id)
        if media_id:
            save_endpoint = '/v4/media/{}/save/{}/'.format(
                media_id, import_id)
            data = {}

        return self.session.post(
            save_endpoint,
            data=data
        )

    def _poll_status(self, import_id):
        """ Gets poll processing status of finalised files.
        """
        for _ in range(MAX_POLLING_ITERATIONS):
            status_dict = self.session.get(
                '/v4/upload/poll/',
                params={'items': [import_id]}
            )

            if [v for k, v in status_dict.items() if import_id in v]:
                return status_dict

            time.sleep(POLLING_IDLE_TIME)

        # Max polling iterations reached => upload failed
        status_dict['itemsFailed'].append(import_id)
        return status_dict
