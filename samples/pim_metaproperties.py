import pprint

from client import BynderClientAuthentication

pp = pprint.PrettyPrinter()

auth_instance = BynderClientAuthentication()
bynder_client = auth_instance.get_auth_client()

# Get the PIM client
pim_client = bynder_client.pim_client
print('\n> Get list of PIM metaproperties:')
pim_metaproperties = pim_client.metaproperties()
pim_metaproperty_id = pim_metaproperties[0]
pp.pprint(pim_metaproperties)


print('\n> Get metaproperty info:')
pim_metaproperty = pim_client.metaproperty_info(
    metaproperty_id=pim_metaproperty_id
)
pp.pprint(pim_metaproperty_id)


print('\n> Get list of PIM metaproperty options:')
pim_metaproperty_options = pim_client.metaproperty_options(
    metaproperty_id=pim_metaproperty_id
)
pim_metaproperty_option_id = pim_metaproperty_options[0]['id']
pp.pprint(pim_metaproperty_options)
