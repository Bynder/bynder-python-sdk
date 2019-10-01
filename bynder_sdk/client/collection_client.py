import json


class CollectionClient:
    """ Client used for all the operations that can be done to collections.
    """
    def __init__(self, oauth2_session):
        self.oauth2_session = oauth2_session

    def collections(self, query: dict = None):
        """ Gets list of the collections.
        """
        return self.oauth2_session.get(
            endpoint='/v4/collections/',
            params=query or {}
        )

    def collection_info(self, collection_id):
        """ Gets all the collection information for a specific collection id.
        """
        return self.oauth2_session.get(
            endpoint='/v4/collections/{0}/'.format(collection_id)
        )

    def create_collection(self, name, query: dict = None):
        """ Creates a collection.
        """
        if query is None:
            query = {}
        query['name'] = name
        return self.oauth2_session.post(
            endpoint='/v4/collections/',
            payload=query
        )

    def delete_collection(self, collection_id):
        """ Deletes a collection.
        """
        return self.oauth2_session.delete(
            endpoint='/v4/collections/{0}/'.format(collection_id)
        )

    def collection_media_ids(self, collection_id):
        """ Gets a list of the media assets ids of a collection.
        """
        return self.oauth2_session.get(
            endpoint='/v4/collections/{0}/media/'.format(collection_id)
        )

    def add_media_to_collection(self, collection_id, media_ids: list):
        """ Adds media assets to a collection.
        """
        query = {
            'data': json.dumps(media_ids)
        }
        return self.oauth2_session.post(
            endpoint='/v4/collections/{0}/media/'.format(collection_id),
            payload=query
        )

    def remove_media_from_collection(self, collection_id, media_ids: list):
        """ Removes media assets from a collection.
        """
        query = {
            'deleteIds': ','.join(map(str, media_ids))
        }
        return self.oauth2_session.delete(
            endpoint='/v4/collections/{0}/media/'.format(collection_id),
            params=query
        )

    def share_collection(self, collection_id, collection_option,
                         recipients: list, query: dict = None):
        """ Shares a collection.
        """
        collection_options = ['view', 'edit']
        if collection_option not in collection_options:
            raise ValueError(
                'Invalid collection_option. Expected one of: {0}'.format(
                    collection_options)
            )
        if query is None:
            query = {}
        query['collectionOptions'] = collection_option
        query['recipients'] = ','.join(map(str, recipients))
        return self.oauth2_session.post(
            endpoint='/v4/collections/{0}/share/'.format(collection_id),
            payload=query
        )
