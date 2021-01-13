from bynder_sdk.client.asset_bank_client import AssetBankClient
from bynder_sdk.client.collection_client import CollectionClient
from bynder_sdk.client.pim_client import PIMClient
from bynder_sdk.client.upload_client import UploadClient
from bynder_sdk.client.workflow_client import WorkflowClient
from bynder_sdk.oauth2 import BynderOAuth2Session


class BynderClient:
    """ Main client used for setting up the OAuth2 session and
    getting the clients for various Bynder modules.
    """

    # pylint: disable-msg=too-many-arguments
    def __init__(
        self,
        domain,
        client_id,
        client_secret,
        scopes,
        redirect_uri=None,
        token=None,
        token_saver=None,
        **kwargs
    ):
        self.session = BynderOAuth2Session(
            domain,
            client_id=client_id,
            client_secret=client_secret,
            scope=scopes,
            redirect_uri=redirect_uri,
            token=token,
            token_updater=token_saver or (lambda _: None)
        )

        self.asset_bank_client = AssetBankClient(self.session)
        self.collection_client = CollectionClient(self.session)
        self.pim_client = PIMClient(self.session)
        self.workflow_client = WorkflowClient(self.session)
        self.upload_client = UploadClient(self.session)

    def get_authorization_url(self):
        return self.session.authorization_url()

    def fetch_token(self, *args, **kwargs):
        return self.session.fetch_token(*args, **kwargs)

    def derivatives(self):
        """ Gets the list of the derivatives configured for the current
        account.
        """
        return self.session.get('/v4/account/derivatives/')
