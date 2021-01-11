from bynder_sdk.client.asset_bank_client import AssetBankClient
from bynder_sdk.client.collection_client import CollectionClient
from bynder_sdk.client.pim_client import PIMClient
from bynder_sdk.client.upload_client import UploadClient
from bynder_sdk.client.workflow_client import WorkflowClient
from bynder_sdk.oauth2 import BynderOAuth2Session

REQUIRED_OAUTH_KWARGS = (
    'client_id', 'client_secret', 'redirect_uri', 'scopes')


class BynderClient:
    """ Main client used for setting up the OAuth2 session and
    getting the clients for various Bynder modules.
    """

    # pylint: disable-msg=too-many-arguments
    def __init__(self, domain, **kwargs):
        missing = [
            kw for kw in REQUIRED_OAUTH_KWARGS
            if kwargs.get(kw) is None
        ]
        if missing:
            raise TypeError(
                'Missing required arguments: {}'.format(missing)
            )

        self.session = BynderOAuth2Session(
            domain,
            kwargs['client_id'],
            scope=kwargs['scopes'],
            redirect_uri=kwargs['redirect_uri'],
            auto_refresh_kwargs={
                'client_id': kwargs['client_id'],
                'client_secret': kwargs['client_secret']
            },
            token_updater=kwargs.get('token_saver', (lambda _: None))
        )

        if kwargs.get('token') is not None:
            self.session.token = kwargs['token']

        self.asset_bank_client = AssetBankClient(self.session)
        self.collection_client = CollectionClient(self.session)
        self.pim_client = PIMClient(self.session)
        self.workflow_client = WorkflowClient(self.session)
        self.upload_client = UploadClient(self.session)

    def get_authorization_url(self):
        return self.session.authorization_url()

    def fetch_token(self, code, *args, **kwargs):
        return self.session.fetch_token(
            code=code,
            *args,
            **kwargs
        )

    def derivatives(self):
        """ Gets the list of the derivatives configured for the current
        account.
        """
        return self.session.get('/v4/account/derivatives/')
