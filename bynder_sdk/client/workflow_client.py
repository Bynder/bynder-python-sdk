class WorkflowClient:
    """ Client used for all the operations that can be done to the workflow module.
    """
    def __init__(self, bynder_request_handler):
        self.bynder_request_handler = bynder_request_handler

    def users(self):
        """ Gets list of users.
        """
        return self.bynder_request_handler.get(
            endpoint='/api/workflow/users/'
        )

    def campaigns(self, query: dict = None):
        """ Gets list of campaigns.
        """
        return self.bynder_request_handler.get(
            endpoint='/api/workflow/campaigns/',
            params=query or {}
        )

    def campaign_info(self, campaign_id):
        """ Gets all the campaign information for a specific campaign id.
        """
        return self.bynder_request_handler.get(
            endpoint='/api/workflow/campaigns/{0}/'.format(campaign_id)
        )

    # pylint: disable=too-many-arguments
    def create_campaign(self, name, key, description, responsible_id,
                        query: dict = None):
        """ Creates a campaign.
        """
        if query is None:
            query = {}
        query.update({
            'name': name,
            'key': key,
            'description': description,
            'responsibleID': responsible_id
        })
        return self.bynder_request_handler.post(
            endpoint='/api/workflow/campaigns/',
            json=query
        )

    def delete_campaign(self, campaign_id):
        """ Deletes a campaign.
        """
        return self.bynder_request_handler.delete(
            endpoint='/api/workflow/campaigns/{0}/'.format(campaign_id)
        )

    def edit_campaign(self, campaign_id, name, key, description,
                      responsible_id, query: dict = None):
        """ Edits an existing campaign.
        """
        if query is None:
            query = {}
        query.update({
            'name': name,
            'key': key,
            'description': description,
            'responsibleID': responsible_id
        })
        return self.bynder_request_handler.put(
            endpoint='/api/workflow/campaigns/{0}/'.format(campaign_id),
            json=query
        )

    def metaproperties(self):
        return self.bynder_request_handler.get(
            endpoint='/api/workflow/metaproperties/'
        )

    def metaproperty_info(self, metaproperty_id):
        return self.bynder_request_handler.get(
            endpoint='/api/workflow/metaproperties/{}/'.format(metaproperty_id)
        )

    def groups(self):
        return self.bynder_request_handler.get(
            endpoint='/api/workflow/groups/'
        )

    def group_info(self, group_id):
        return self.bynder_request_handler.get(
            endpoint='/api/workflow/groups/{}/'.format(group_id)
        )

    def job_preset_info(self, job_preset_id):
        return self.bynder_request_handler.get(
            endpoint='/api/workflow/presets/job/{}/'.format(job_preset_id)
        )

    def jobs(self, campaign_id: str = None):
        if campaign_id:
            return self.bynder_request_handler.get(
                endpoint='/api/workflow/campaigns/{}/jobs/'.format(campaign_id)
            )
        return self.bynder_request_handler.get(
            endpoint='/api/workflow/jobs/'
        )

    def create_job(self, name, campaign_id, accountable_id,
                   preset_id, query: dict = None):
        if query is None:
            query = {}
        query.update({
            'name': name,
            'campaignID': campaign_id,
            'accountableID': accountable_id,
            'presetID': preset_id
        })
        return self.bynder_request_handler.post(
            endpoint='/api/workflow/jobs/',
            json=query
        )

    def job_info(self, job_id):
        return self.bynder_request_handler.get(
            endpoint='/api/workflow/jobs/{}/'.format(job_id)
        )

    def edit_job(self, job_id, name, campaign_id, accountable_id,
                 preset_id, query: dict = None):
        if query is None:
            query = {}
        query.update({
            'name': name,
            'campaignID': campaign_id,
            'accountableID': accountable_id,
            'presetID': preset_id
        })
        return self.bynder_request_handler.put(
            endpoint='/api/workflow/jobs/{}/'.format(job_id),
            json=query
        )

    def delete_job(self, job_id):
        return self.bynder_request_handler.delete(
            endpoint='/api/workflow/jobs/{}/'.format(job_id)
        )
