from urllib.parse import (urljoin, parse_qs)
import requests
from requests_oauthlib import OAuth1


class OauthRequestHandler:
    """ Handles the creation of an authorisation header and the execution
    of GET, POST and DELETE requests.
    """
    def __init__(self, base_url, request_credentials):
        self.base_url = base_url
        self._credentials = request_credentials

    @property
    def credentials(self):
        return self._credentials

    @credentials.setter
    def credentials(self, request_credentials):
        self._credentials = request_credentials

    @property
    def oauth(self):
        return OAuth1(
            client_key=self.credentials.consumer_key,
            client_secret=self.credentials.consumer_secret,
            resource_owner_key=self.credentials.token,
            resource_owner_secret=self.credentials.token_secret,
            signature_type="auth_header"
        )

    def fetch_token(self, endpoint):
        response = requests.post(
            urljoin(self.base_url, endpoint),
            auth=self.oauth
        )
        response.raise_for_status()
        return parse_qs(response.content.decode('UTF-8'))

    def _generic_request(self, request_type, endpoint, payload: dict = None, params: dict = None):
        """ Generic method used for Bynder requests
        """
        response = request_type(
            urljoin(self.base_url, endpoint),
            auth=self.oauth,
            params=params,
            data=payload,
            verify=True
        )
        response.raise_for_status()
        try:
            return response.json()
        except ValueError:
            return {}

    def get(self, endpoint, params: dict = None):
        """ Send GET request to user portal.
        """
        return self._generic_request(
            requests.get,
            endpoint,
            params=params
        )

    def post(self, endpoint, payload: dict = None):
        """ Send POST request to user portal.
        """
        return self._generic_request(
            request_type=requests.post,
            endpoint=endpoint,
            payload=payload
        )

    def delete(self, endpoint, payload: dict = None, params: dict = None):
        """ Send DELETE request to user portal.
        """
        return self._generic_request(
            request_type=requests.delete,
            endpoint=endpoint,
            payload=payload,
            params=params
        )

    @staticmethod
    def post_file(upload_url, files, payload):
        response = requests.post(
            upload_url,
            files=files,
            data=payload
        )
        response.raise_for_status()
        return response
