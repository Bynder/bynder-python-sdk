from bynder_sdk.client.bynder_client import BynderClient

TOKEN = 'token'
TEST_DOMAIN = 'test.getbynder.com'


def create_bynder_client():
    return BynderClient(
        domain=TEST_DOMAIN,
        redirect_uri='https://test.com/',
        client_id='client_id',
        client_secret='client_secret',
        token=TOKEN,
        scopes='offline'
    )
