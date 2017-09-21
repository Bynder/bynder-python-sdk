import time
import configparser
from bynder_sdk import BynderClient

# Get your tokens from .ini file
config = configparser.ConfigParser()
config.read('settings.ini')

HAS_TOKENS = False

# Create the BynderClient with your tokens
bynder_client = BynderClient(
    base_url=config.get('api', 'url'),
    consumer_key=config.get('oauth', 'consumer_key'),
    consumer_secret=config.get('oauth', 'consumer_secret'),
    token=config.get('oauth', 'token'),
    token_secret=config.get('oauth', 'token_secret')
)

# Generate tokens if you don't have them
if not HAS_TOKENS:
    # Generate request token
    bynder_client.request_token()

    # Get the authorise url
    authorise_url = bynder_client.authorise_url()
    print(authorise_url)

    # Sleep for a while to give you time to login using the authorise url
    time.sleep(20)

    # Now get the access tokens
    bynder_client.access_token()

    # Or use the login method (deprecated)
    # login = bynder_client.login(
    #     username='your_username',
    #     password='your_password'
    # )
    # print(login)


# Get the asset bank client
asset_bank_client = bynder_client.asset_bank_client


# Get the collections client
collection_client = bynder_client.collection_client


# Get brands
brands = asset_bank_client.brands()
print(brands)


# Get tags
tags = asset_bank_client.tags()
print(tags)


# Get meta properties
meta_properties = asset_bank_client.meta_properties()
print(meta_properties)


# Get media list
media_list = asset_bank_client.media_list({
    'count': True,
    'limit': 2,
    'type': 'image',
    'versions': 1
})
print(media_list)


# Get media info
media_id = media_list.get('media')[0].get('id')
media_info = asset_bank_client.media_info(
    media_id=media_id,
    versions={
        'versions': 1
    }
)
print(media_info)


# Get download url
download_url = asset_bank_client.media_download_url(
    media_id=media_id
)
print(download_url)


# Get collections list
collections = collection_client.collections()
print(collections)


# Get media ids of a collection
collection_id = collections[0]['id']
collection_media_ids = collection_client.collection_media_ids(
    collection_id=collection_id
)
print(collection_media_ids)
