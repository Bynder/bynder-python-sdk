import pprint

from client import BynderClientAuthentication

pp = pprint.PrettyPrinter()

auth_instance = BynderClientAuthentication()
bynder_client = auth_instance.get_auth_client()

# Get the workflow client
workflow_client = bynder_client.workflow_client
print('\n> Get campaigns list:')
campaigns = workflow_client.campaigns()

print('\n> Get campaign ID:')
campaign_id = campaigns[0]['ID']
pp.pprint(campaign_id)

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
