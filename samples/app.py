import pprint

from bynder_sdk import BynderClient

pp = pprint.PrettyPrinter()

# When using Permanent Tokens

bynder_client = BynderClient(
    domain='portal.getbynder.com',
    permanent_token=''
)

# When using OAuth2

token = None
""" If we already have a token, it can be passed to the BynderClient
initialization.

    token = {
        'access_token': '...',
        'expires_at': 123456789,
        'expires_in': 3599,
        'id_token': '...',
        'refresh_token': '...',
        'scope': ['offline'],
        'token_type': 'bearer'
    }
"""


def token_saver(token):
    """ This function will be called by oauthlib-requests when a new
    token is retrieved, either after the initial login or refreshing an
    existing token. """
    print('New token received:')
    pp.pprint(token)


bynder_client = BynderClient(
    domain='portal.getbynder.com',
    redirect_uri='',
    client_id='',
    client_secret='',
    scopes=['offline', 'asset:read', 'meta.assetbank:read'],
    token=token,  # optional, if we already have one
    token_saver=token_saver,  # optional, defaults to empty lambda
)

if token is None:
    pp.pprint(bynder_client.get_authorization_url())

    code = input('Code: ')
    pp.pprint(bynder_client.fetch_token(code))

# Example calls

# Get the asset bank client
asset_bank_client = bynder_client.asset_bank_client


# Get the collections client
collection_client = bynder_client.collection_client


# Get the workflow client
workflow_client = bynder_client.workflow_client


# Get the PIM client
pim_client = bynder_client.pim_client


print('\n> Get brands:')
brands = asset_bank_client.brands()
pp.pprint(brands)


print('\n> Get tags:')
tags = asset_bank_client.tags()
pp.pprint(tags)


print('\n> Get metaproperties:')
meta_properties = asset_bank_client.meta_properties()
pp.pprint(meta_properties)


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


print('\n> Get collections list:')
collections = collection_client.collections()
pp.pprint(collections)


print('\n> Get media ids of a collection:')
collection_id = collections[0]['id']
collection_media_ids = collection_client.collection_media_ids(
    collection_id=collection_id
)
pp.pprint(collection_media_ids)


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


print('\n> Get workflow metaproperties list:')
workflow_metaproperties = workflow_client.metaproperties()
workflow_metaproperty_id = workflow_metaproperties[0]['ID']
pp.pprint(workflow_metaproperties)


print('\n> Get workflow metaproperty info:')
workflow_metaproperty = workflow_client.metaproperty_info(
    metaproperty_id=workflow_metaproperty_id)
pp.pprint(workflow_metaproperty)


print('\n> Get workflow groups list:')
workflow_groups = workflow_client.groups()
workflow_group_id = workflow_groups[0]['ID']
pp.pprint(workflow_groups)


print('\n> Get workflow group info:')
workflow_group = workflow_client.group_info(
    group_id=workflow_group_id
)
pp.pprint(workflow_group)


print('\n> Get jobs:')
jobs = workflow_client.jobs()
job_id = jobs[0]['id']
pp.pprint(jobs)


print('\n> Get jobs by campaign:')
jobs_by_campaign = workflow_client.jobs(
    campaign_id=campaign_id
)
pp.pprint(jobs_by_campaign)


print('\n> Get specific job:')
job_info = workflow_client.job_info(
    job_id=job_id
)
pp.pprint(job_info)


print('\n> Create new job:')
new_job = workflow_client.create_job(
    name='new_job_name',
    campaign_id=job_info['campaignID'],
    accountable_id=job_info['accountableID'],
    preset_id=job_info['presetID']
)
pp.pprint(new_job)


print('\n> Edit job:')
edited_job = workflow_client.edit_job(
    job_id,
    name='edited_job_name',
    campaign_id=job_info['campaignID'],
    accountable_id=job_info['accountableID'],
    preset_id=job_info['presetID']
)
pp.pprint(edited_job)


print('\n> Delete job:')
workflow_client.delete_job(
    job_id=job_id
)


print('\n> Get job preset info:')
job_preset_info = workflow_client.job_preset_info(
    job_preset_id=job_info['presetID']
)
pp.pprint(job_preset_info)


print('\n> Upload a file to the asset bank')
uploaded_file = asset_bank_client.upload_file(
    file_path='example/image.png',
    brand_id=brands[0]['id']
)

pp.pprint(uploaded_file)
