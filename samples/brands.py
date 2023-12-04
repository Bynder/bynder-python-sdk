import pprint

from client import BynderClientAuthentication

pp = pprint.PrettyPrinter()

auth_instance = BynderClientAuthentication()
bynder_client = auth_instance.get_auth_client()

# Get the asset bank client
asset_bank_client = bynder_client.asset_bank_client
print('\n> Get brands:')
brands = asset_bank_client.brands()
pp.pprint(brands)
