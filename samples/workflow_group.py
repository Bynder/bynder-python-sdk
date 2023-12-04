import pprint

from client import BynderClientAuthentication

pp = pprint.PrettyPrinter()

auth_instance = BynderClientAuthentication()
bynder_client = auth_instance.get_auth_client()

# Get the workflow client
workflow_client = bynder_client.workflow_client
print('\n> Get workflow groups list:')
workflow_groups = workflow_client.groups()
workflow_group_id = workflow_groups[0]['ID']
pp.pprint(workflow_groups)


print('\n> Get workflow group info:')
workflow_group = workflow_client.group_info(
    group_id=workflow_group_id
)
pp.pprint(workflow_group)
