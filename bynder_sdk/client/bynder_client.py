from bynder_sdk.client.asset_bank_client import AssetBankClient
from bynder_sdk.client.collection_client import CollectionClient
from bynder_sdk.client.pim_client import PIMClient
from bynder_sdk.client.workflow_client import WorkflowClient
from bynder_sdk.oauth2 import BynderOAuth2Session


class BynderClient:
    """ Main client used for setting up the OAuth2 session and
    getting the clients for various Bynder modules.
    """

    DEFAULT_SCOPES = ['openid', 'offline']

    # pylint: disable-msg=too-many-arguments
    def __init__(self, domain, client_id, client_secret, redirect_uri,
                 token=None, token_saver=None, scopes=None):
        self.oauth2_session = BynderOAuth2Session(
            domain,
            client_id,
            scope=scopes or BynderClient.DEFAULT_SCOPES,
            redirect_uri=redirect_uri,
            auto_refresh_kwargs={
                'client_id': client_id,
                'client_secret': client_secret
            },
            token_updater=token_saver or (lambda _: None)
        )

        if token is not None:
            self.oauth2_session.token = token

        self.asset_bank_client = AssetBankClient(self.oauth2_session)
        self.collection_client = CollectionClient(self.oauth2_session)
        self.pim_client = PIMClient(self.oauth2_session)
        self.workflow_client = WorkflowClient(self.oauth2_session)

    def get_authorization_url(self):
        return self.oauth2_session.authorization_url()

    def fetch_token(self, code, *args, **kwargs):
        return self.oauth2_session.fetch_token(
            code=code,
            *args,
            **kwargs
        )

    def derivatives(self):
        """ Gets the list of the derivatives configured for the current account.
        """
        return self.oauth2_session.get('/v4/account/derivatives/')
