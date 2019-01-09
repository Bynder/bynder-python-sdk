import configparser
import time
import webbrowser

from bynder_sdk import BynderClient

# Get your tokens from .ini file
config = configparser.ConfigParser()
config.read('settings.ini')

HAS_TOKENS = False

# Create the BynderClient with your tokens
bynder_client = BynderClient(
    base_url=config.get('api', 'url'),
    consumer_key=config.get('oauth', 'consumer_key'),
    consumer_secret=config.get('oauth', 'consumer_secret'),
    token=config.get('oauth', 'token'),
    token_secret=config.get('oauth', 'token_secret')
)

# Generate tokens if you don't have them
if not HAS_TOKENS:
    # Generate request token
    bynder_client.request_token()

    # Get the authorise url
    authorise_url = bynder_client.authorise_url()
    print(authorise_url)
    webbrowser.open_new_tab(authorise_url)

    # Sleep for a while to give you time to login using the authorise url
    time.sleep(20)

    # Now get the access tokens
    bynder_client.access_token()

    # Or use the login method (deprecated)
    # login = bynder_client.login(
    #     username='your_username',
    #     password='your_password'
    # )
    # print(login)


# Get the asset bank client
asset_bank_client = bynder_client.asset_bank_client


# Get the collections client
collection_client = bynder_client.collection_client


# Get the workflow client
workflow_client = bynder_client.workflow_client


# Get the PIM client
pim_client = bynder_client.pim_client


# Get brands
brands = asset_bank_client.brands()
print(brands)


# Get tags
tags = asset_bank_client.tags()
print(tags)


# Get meta properties
meta_properties = asset_bank_client.meta_properties()
print(meta_properties)


# Get media list
media_list = asset_bank_client.media_list({
    'count': True,
    'limit': 2,
    'type': 'image',
    'versions': 1
})
print(media_list)


# Get media info
media_id = media_list.get('media')[0].get('id')
media_info = asset_bank_client.media_info(
    media_id=media_id,
    versions={
        'versions': 1
    }
)
print(media_info)


# Get download url
download_url = asset_bank_client.media_download_url(
    media_id=media_id
)
print(download_url)


# Get collections list
collections = collection_client.collections()
print(collections)


# Get media ids of a collection
collection_id = collections[0]['id']
collection_media_ids = collection_client.collection_media_ids(
    collection_id=collection_id
)
print(collection_media_ids)


# Get workflow users
workflow_users = workflow_client.users()
workflow_user = workflow_users[0]['ID']
print(workflow_users)


# Create new campaign
new_campaign = workflow_client.create_campaign(
    name='compaign_name',
    key='CKEY',
    description='campaign_description',
    responsible_id=workflow_user
)
print(new_campaign)


# Get campaigns list
campaigns = workflow_client.campaigns()
print(campaigns)


# Get campaign info
campaign_id = campaigns[0]['ID']
campaign_info = workflow_client.campaign_info(campaign_id)
print(campaign_info)


# Edit a campaign
edited_campaign = workflow_client.edit_campaign(
    campaign_id=new_campaign['id'],
    name='new_compaign_name',
    key='NCKEY',
    description='new_compaign_description',
    responsible_id=workflow_user
)
print(edited_campaign)


# Delete campaign
workflow_client.delete_campaign(
    campaign_id=new_campaign['id']
)


# Get list of PIM metaproperties
pim_metaproperties = pim_client.metaproperties()
pim_metaproperty_id = pim_metaproperties[0]
print(pim_metaproperties)


# Get metaproperty info
pim_metaproperty = pim_client.metaproperty_info(
    metaproperty_id=pim_metaproperty_id
)
print(pim_metaproperty_id)


# Get list of PIM metapropery options
pim_metaproperty_options = pim_client.metaproperty_options(
    metaproperty_id=pim_metaproperty_id
)
pim_metaproperty_option_id = pim_metaproperty_options[0]['id']
print(pim_metaproperty_options)


# Get workflow metaproperties list
workflow_metaproperties = workflow_client.metaproperties()
workflow_metaproperty_id = workflow_metaproperties[0]['ID']
print(workflow_metaproperties)


# Get workflow metaproperty info
workflow_metaproperty = workflow_client.metaproperty_info(
    metaproperty_id=workflow_metaproperty_id)
print(workflow_metaproperty)


# Get workflow groups list
workflow_groups = workflow_client.groups()
workflow_group_id = workflow_groups[0]['ID']
print(workflow_groups)


# Get workflow group info
workflow_group = workflow_client.group_info(
    group_id=workflow_group_id
)
print(workflow_group)


# Get jobs
jobs = workflow_client.jobs()
job_id = jobs[0]['id']
print(jobs)


# Get jobs by campaign
jobs_by_campaign = workflow_client.jobs(
    campaign_id=campaign_id
)
print(jobs_by_campaign)


# Get specific job
job_info = workflow_client.job_info(
    job_id=job_id
)
print(job_info)


# Create new job
new_job = workflow_client.create_job(
    name='new_job_name',
    campaign_id=job_info['campaignID'],
    accountable_id=job_info['accountableID'],
    preset_id=job_info['presetID']
)
print(new_job)


# Edit job
edited_job = workflow_client.edit_job(
    job_id,
    name='edited_job_name',
    campaign_id=job_info['campaignID'],
    accountable_id=job_info['accountableID'],
    preset_id=job_info['presetID']
)
print(edited_job)


# Delete job
workflow_client.delete_job(
    job_id=job_id
)


# Get job preset info
job_preset_info = workflow_client.job_preset_info(
    job_preset_id=job_info['presetID']
)
print(job_preset_info)
