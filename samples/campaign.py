import pprint

from client import BynderClientAuthentication

pp = pprint.PrettyPrinter()

auth_instance = BynderClientAuthentication()
bynder_client = auth_instance.get_auth_client()

# Get the workflow client
workflow_client = bynder_client.workflow_client
print('\n> Get workflow users:')
workflow_users = workflow_client.users()
workflow_user = workflow_users[0]['ID']
pp.pprint(workflow_users)

print('\n> Create new campaign:')
new_campaign = workflow_client.create_campaign(
    name='compaign_name',
    key='CKEY',
    description='campaign_description',
    responsible_id=workflow_user
)
pp.pprint(new_campaign)


print('\n> Get campaigns list:')
campaigns = workflow_client.campaigns()
pp.pprint(campaigns)


print('\n> Get campaigns info:')
campaign_id = campaigns[0]['ID']
campaign_info = workflow_client.campaign_info(campaign_id)
pp.pprint(campaign_info)


print('\n> Edit a campaign:')
edited_campaign = workflow_client.edit_campaign(
    campaign_id=new_campaign['id'],
    name='new_compaign_name',
    key='NCKEY',
    description='new_compaign_description',
    responsible_id=workflow_user
)
pp.pprint(edited_campaign)


print('\n> Delete campaign:')
workflow_client.delete_campaign(
    campaign_id=new_campaign['id']
)