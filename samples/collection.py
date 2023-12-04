import pprint

from client import BynderClientAuthentication

pp = pprint.PrettyPrinter()

auth_instance = BynderClientAuthentication()
bynder_client = auth_instance.get_auth_client()

# Get the collections client
collection_client = bynder_client.collection_client
print('\n> Get collections list:')
collections = collection_client.collections()
pp.pprint(collections)


print('\n> Get media ids of a collection:')
collection_id = collections[0]['id']
collection_media_ids = collection_client.collection_media_ids(
    collection_id=collection_id
)
pp.pprint(collection_media_ids)
