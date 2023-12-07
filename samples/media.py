import pprint

from client import BynderClientAuthentication

pp = pprint.PrettyPrinter()

auth_instance = BynderClientAuthentication()
bynder_client = auth_instance.get_auth_client()

# Get the asset bank client
asset_bank_client = bynder_client.asset_bank_client
print('\n> Get media list:')
media_list = asset_bank_client.media_list({
    'count': True,
    'limit': 2,
    'type': 'image',
    'versions': 1
})
pp.pprint(media_list)


print('\n> Get media info:')
media_id = media_list.get('media')[0].get('id')
media_info = asset_bank_client.media_info(
    media_id=media_id,
    versions={
        'versions': 1
    }
)
pp.pprint(media_info)

print('\n Set media description:')
media = asset_bank_client.set_media_properties(
    media_id,
    {'description': 'Description set using SDK'}
)

print('\n> Get download url:')
download_url = asset_bank_client.media_download_url(
    media_id=media_id
)
pp.pprint(download_url)

