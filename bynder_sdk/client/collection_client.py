import json


class CollectionClient:
    """ Client used for all the operations that can be done to collections.
    """
    def __init__(self, session):
        self.session = session

    def collections(self, query: dict = None):
        """ Gets list of the collections.
        """
        return self.session.get('/v4/collections/', params=query or {})

    def collection_info(self, collection_id):
        """ Gets all the collection information for a specific collection id.
        """
        return self.session.get(f'/v4/collections/{collection_id}/')

    def create_collection(self, name, query: dict = None):
        """ Creates a collection.
        """
        if query is None:
            query = {}
        query['name'] = name
        return self.session.post('/v4/collections/', data=query)

    def delete_collection(self, collection_id):
        """ Deletes a collection.
        """
        return self.session.delete(
            f'/v4/collections/{collection_id}/'
        )

    def collection_media_ids(self, collection_id):
        """ Gets a list of the media assets ids of a collection.
        """
        return self.session.get(
            f'/v4/collections/{collection_id}/media/'
        )

    def add_media_to_collection(self, collection_id, media_ids: list):
        """ Adds media assets to a collection.
        """
        query = {
            'data': json.dumps(media_ids)
        }
        return self.session.post(
            f'/v4/collections/{collection_id}/media/',
            data=query
        )

    def remove_media_from_collection(self, collection_id, media_ids: list):
        """ Removes media assets from a collection.
        """
        query = {
            'deleteIds': ','.join(map(str, media_ids))
        }
        return self.session.delete(
            f'/v4/collections/{collection_id}/media/',
            params=query
        )

    def share_collection(self, collection_id, collection_option,
                         recipients: list, query: dict = None):
        """ Shares a collection.
        """
        collection_options = ['view', 'edit']
        if collection_option not in collection_options:
            raise ValueError(
                f'Invalid collection_option. Expected one of: '
                f'{collection_options}'
            )
        if query is None:
            query = {}
        query['collectionOptions'] = collection_option
        query['recipients'] = ','.join(map(str, recipients))
        return self.session.post(
            f'/v4/collections/{collection_id}/share/',
            data=query
        )
