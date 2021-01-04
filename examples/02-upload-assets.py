import pprint
import time

from requests.exceptions import HTTPError

try:
    from .util import get_client
except ImportError:
    from util import get_client


pp = pprint.PrettyPrinter()


def main():
    client = get_client(scopes=['asset:write', 'asset:read'])
    asset_bank_client = client.asset_bank_client

    # When a portal has multiple brands, passing brand_id to the upload
    # call is required. If your portal only has one brand, you can skip
    # this step.
    print('> Retrieving brands')
    brands = client.asset_bank_client.brands()
    pp.pprint(brands)

    # Upload our file
    print('> Uploading {}'.format('example/image.png'))
    uploaded_file = asset_bank_client.upload_file(
        file_path='example/image.png',
        brand_id=brands[0]['id']
    )

    pp.pprint(uploaded_file)

    # After completing the upload, it may take a few seconds before
    # it can be fetched using the get_media method.
    print('> Querying for created asset')
    asset = None
    while asset is None:
        try:
            asset = asset_bank_client.media_info(uploaded_file['mediaid'])
        except HTTPError as exc:
            if exc.response.status_code != 404:
                raise

            print('Asset not available yet..')
            time.sleep(1)

    pp.pprint(asset)

    print('> Uploading a new version for the created asset')
    uploaded_version = asset_bank_client.upload_file(
        file_path='example/image.png',
        brand_id=brands[0]['id'],
        media_id=asset['id']
    )
    pp.pprint(uploaded_version)


if __name__ == '__main__':
    main()
