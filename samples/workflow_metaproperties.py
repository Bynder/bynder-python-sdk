import pprint

from client import BynderClientAuthentication

pp = pprint.PrettyPrinter()

auth_instance = BynderClientAuthentication()
bynder_client = auth_instance.get_auth_client()

# Get the workflow client
workflow_client = bynder_client.workflow_client
print('\n> Get workflow metaproperties list:')
workflow_metaproperties = workflow_client.metaproperties()
workflow_metaproperty_id = workflow_metaproperties[0]['ID']
pp.pprint(workflow_metaproperties)


print('\n> Get workflow metaproperty info:')
workflow_metaproperty = workflow_client.metaproperty_info(
    metaproperty_id=workflow_metaproperty_id)
pp.pprint(workflow_metaproperty)
