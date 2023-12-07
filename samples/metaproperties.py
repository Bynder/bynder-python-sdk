import pprint

from client import BynderClientAuthentication

pp = pprint.PrettyPrinter()

auth_instance = BynderClientAuthentication()
bynder_client = auth_instance.get_auth_client()

# Get the asset bank client
asset_bank_client = bynder_client.asset_bank_client
print('\n> Get metaproperties:')
meta_properties = asset_bank_client.meta_properties()
pp.pprint(meta_properties)
