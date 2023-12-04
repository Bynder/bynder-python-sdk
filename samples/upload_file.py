import pprint

from client import BynderClientAuthentication

pp = pprint.PrettyPrinter()

auth_instance = BynderClientAuthentication()
bynder_client = auth_instance.get_auth_client()

# Get the asset bank client
asset_bank_client = bynder_client.asset_bank_client
print('\n> Get brands:')
brands = asset_bank_client.brands()

print('\n> Get brand ID:')
brand_id = brands[0]['id']
pp.pprint(brand_id)

print('\n> Upload a file to the asset bank')
uploaded_file = asset_bank_client.upload_file(
    file_path='samples/image.png',
    brand_id=brand_id
)

pp.pprint(uploaded_file)
