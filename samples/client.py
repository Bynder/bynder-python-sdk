import json

from bynder_sdk import BynderClient


class BynderClientAuthentication:

    def __init__(self, config_file_path='secret.json'):
        with open(config_file_path, 'r') as file:
            self.config_data = json.load(file)

    def token_saver(token):
        """ This function will be called by oauthlib-requests when a new
        token is retrieved, either after the initial login or refreshing an
        existing token. """
        print('New token received:')
        print(token)

    def get_auth_client(self) -> BynderClient:
        # When using Permanent Tokens
        if self.config_data.get('permanent_token', None):
            return BynderClient(
                domain=self.config_data.get('domain', None),
                permanent_token=self.config_data.get('permanent_token', None)
            )

        # When using OAuth2
        bynder_client = BynderClient(
            **self.config_data,
            token_saver=self.token_saver,  # optional, defaults to empty lambda
        )
        # Token object example
        #     token = {
        #         "access_token": "...",
        #         "expires_at": 123456789,
        #         "expires_in": 3599,
        #         "id_token": "...",
        #         "refresh_token": "...",
        #         "scope": ["offline"],
        #         "token_type": "bearer"
        #     }

        # auth code grant type
        if self.config_data.get('token', None) is None and self.config_data.get('client_credentials', None) is None:
            print(bynder_client.get_authorization_url())

            code = input('Code: ')
            print(bynder_client.fetch_token(code))

        # client credentials grant type
        elif self.config_data.get('token', None) is None and self.config_data.get('client_credentials', None):
            bynder_client.fetch_token(code=None)

        return bynder_client
