from unittest import mock, TestCase

from test import create_bynder_client


class WorkflowClientTest(TestCase):
    """ Test the workflow client.
    """
    def setUp(self):
        self.bynder_client = create_bynder_client()

        self.workflow_client = self.bynder_client.workflow_client
        self.workflow_client.session.get = mock.MagicMock()
        self.workflow_client.session.post = mock.MagicMock()
        self.workflow_client.session.delete = mock.MagicMock()
        self.workflow_client.session.put = mock.MagicMock()

    def tearDown(self):
        self.bynder_client = None
        self.workflow_client = None

    def test_users(self):
        """ Test if when we call workflow users it will use the correct params for
        the request and returns successfully.
        """
        self.workflow_client.users()
        self.workflow_client.session.get.assert_called_with(
            endpoint='/workflow/users/'
        )

    def test_campaigns(self):
        """ Test if when we call campaigns it will use the correct params for the
        request and returns successfully.
        """
        self.workflow_client.campaigns()
        self.workflow_client.session.get.assert_called_with(
            endpoint='/workflow/campaigns/',
            params={}
        )

    def test_campaign_info(self):
        """ Test if when we call campaign info it will use the correct params for the
        request and returns successfully.
        """
        self.workflow_client.campaign_info(campaign_id=1111)
        self.workflow_client.session.get.assert_called_with(
            endpoint='/workflow/campaigns/1111/'
        )

    def test_create_campaign(self):
        """ Test if when we call create a campaign it will use the correct params for
        the request and returns successfully.
        """
        self.workflow_client.create_campaign(
            name='campaign_name',
            key='CKEY',
            description='campaign_description',
            responsible_id='campaign_responsible_id'
        )
        self.workflow_client.session.post.assert_called_with(
            endpoint='/workflow/campaigns/',
            json={
                'name': 'campaign_name',
                'key': 'CKEY',
                'description': 'campaign_description',
                'responsibleID': 'campaign_responsible_id'
            }
        )

    def test_edit_campaign(self):
        """ Test if when we call edit campaign it will use the correct params for
        the request and returns successfully.
        """
        self.workflow_client.edit_campaign(
            campaign_id='campaign_id',
            name='campaign_name',
            key='ECKEY',
            description='campaign_description',
            responsible_id='campaign_responsible_id'
        )
        self.workflow_client.session.put.assert_called_with(
            endpoint='/workflow/campaigns/campaign_id/',
            json={
                'name': 'campaign_name',
                'key': 'ECKEY',
                'description': 'campaign_description',
                'responsibleID': 'campaign_responsible_id'
            }
        )

    def test_delete_campaign(self):
        """ Test if when we call delete campaign it will use the correct params for the
        request and returns successfully.
        """
        self.workflow_client.delete_campaign(campaign_id=1111)
        self.workflow_client.session.delete.assert_called_with(
            endpoint='/workflow/campaigns/1111/'
        )

    def test_metaproperties(self):
        """ Test if when we call metaproperties it will use the correct params for
        the request and returns successfully.
        """
        self.workflow_client.metaproperties()
        self.workflow_client.session.get.assert_called_with(
            endpoint='/workflow/metaproperties/'
        )

    def test_metaproperty_info(self):
        """ Test if when we call metaproperty info it will use the correct params
        for the request and returns successfully
        """
        self.workflow_client.metaproperty_info(metaproperty_id=1111)
        self.workflow_client.session.get.assert_called_with(
            endpoint='/workflow/metaproperties/{}/'.format(1111)
        )

    def test_groups(self):
        """ Test if when we call groups it will use the correct params for the
        request and returns successfully.
        """
        self.workflow_client.groups()
        self.workflow_client.session.get.assert_called_with(
            endpoint='/workflow/groups/'
        )

    def test_group_info(self):
        """ Test if when we call group info it will use the correct params for the
        request and returns successfully.
        """
        self.workflow_client.group_info(1111)
        self.workflow_client.session.get.assert_called_with(
            endpoint='/workflow/groups/{}/'.format(1111)
        )

    def test_job_preset_info(self):
        """ Test if when we call job preset info it will use the correct params for
        the request and returns successfully.
        """
        self.workflow_client.job_preset_info(job_preset_id=1111)
        self.workflow_client.session.get.assert_called_with(
            endpoint='/workflow/presets/job/{}/'.format(1111)
        )

    def test_jobs(self):
        """ Test if when we call jobs it will use the correct params for the
        request and returns successfully.
        """
        self.workflow_client.jobs(campaign_id=1111)
        self.workflow_client.session.get.assert_called_with(
            endpoint='/workflow/campaigns/{}/jobs/'.format(1111)
        )
        self.workflow_client.jobs()
        self.workflow_client.session.get.assert_called_with(
            endpoint='/workflow/jobs/'
        )

    def test_create_job(self):
        """ Test if when we call create job it will use the correct params for the
        request and returns successfully.
        """
        self.workflow_client.create_job(
            name='job_name',
            campaign_id='job_campaign_id',
            accountable_id='job_accountable_id',
            preset_id='job_preset_id'
        )
        self.workflow_client.session.post.assert_called_with(
            endpoint='/workflow/jobs/',
            json={
                'name': 'job_name',
                'campaignID': 'job_campaign_id',
                'accountableID': 'job_accountable_id',
                'presetID': 'job_preset_id'
            }
        )

    def test_job_info(self):
        """ Test if when we call job info it will use the correct params for the
        request and returns successfully.
        """
        self.workflow_client.job_info(job_id='1111')
        self.workflow_client.session.get.assert_called_with(
            endpoint='/workflow/jobs/{}/'.format(1111)
        )

    def test_edit_job(self):
        """ Test if when we call edit job it will use the correct params for the
        request and returns successfully.
        """
        self.workflow_client.edit_job(
            job_id=1111,
            name='job_name',
            campaign_id='job_campaign_id',
            accountable_id='job_accountable_id',
            preset_id='job_preset_id'
        )
        self.workflow_client.session.put.assert_called_with(
            endpoint='/workflow/jobs/{}/'.format(1111),
            json={
                'name': 'job_name',
                'campaignID': 'job_campaign_id',
                'accountableID': 'job_accountable_id',
                'presetID': 'job_preset_id'
            }
        )

    def test_delete_job(self):
        """ Test if when we call delete job it will use the correct params for the
        request and returns successfully.
        """
        self.workflow_client.delete_job(job_id=1111)
        self.workflow_client.session.delete(
            endpoint='/workflow/jobs/{}/'.format(1111)
        )
