import pprint

from client import BynderClientAuthentication

pp = pprint.PrettyPrinter()

auth_instance = BynderClientAuthentication()
bynder_client = auth_instance.get_auth_client()

# Get the collections client
collection_client = bynder_client.collection_client
print('\n> Create a new collection:')
new_collection = collection_client.create_collection(
    name='testing collection python sdk'
)
pp.pprint(new_collection)

print('\n> Get collections list:')
collections = collection_client.collections(query={'keyword': 'testing collection python sdk'})
collection_id = collections[0]['id']
pp.pprint(collections)

print('\n> Get specific collection info:')
collection = collection_client.collection_info(collection_id)
pp.pprint(collection)


# Get the asset bank client to get media id
asset_bank_client = bynder_client.asset_bank_client
media_list = asset_bank_client.media_list({
    'count': True,
    'limit': 2,
    'type': 'image',
    'versions': 1
})
media_id = media_list.get('media')[0].get('id')

print('\n> Add media assets to specific collection:')
collection = collection_client.add_media_to_collection(
    collection_id,
    media_ids=[media_id]
)
pp.pprint(collection)

print('\n> Get media ids of a collection:')
collection_media_ids = collection_client.collection_media_ids(
    collection_id=collection_id
)
pp.pprint(collection_media_ids)

print('\n> Remove media from specific collection:')
collection = collection_client.remove_media_from_collection(
    collection_id,
    media_ids=[media_id]
)
pp.pprint(collection)

print('\n> Delete a collection:')
deleted_collection = collection_client.delete_collection(
    collection_id=collection_id
)
pp.pprint(deleted_collection)
