import os
import pprint
from configparser import ConfigParser

pp = pprint.PrettyPrinter()

try:
    from bynder_sdk import BynderClient
except ModuleNotFoundError as exc:
    raise RuntimeError(
        'Please run pip install . before running the examples') from exc

FLOWS = {
    'token': {'domain', 'access_token'},
    'authorization_code': {
        'domain', 'client_id', 'client_secret', 'redirect_uri'},
    'client_credentials': {'domain', 'client_id', 'client_secret'}
}

# Generate set of used config keys in all flows
CONFIG_KEYS = {key for sublist in FLOWS.values() for key in sublist}


def token_saver(token):
    """ This function will be called by oauthlib-requests when a new
    token is retrieved, either after the initial login or refreshing an
    existing token. """
    print('New token received:')
    pp.pprint(token)


def get_client(scopes):
    print('> Creating instance of BynderClient and go through ' +
          'authorization code flow if necessary.')
    config = ConfigParser()
    config.read(
        os.path.join(os.path.dirname(__file__), 'config.ini')
    )

    # Build a dictionary based on the config file and environment variables
    portal_config = {
        'scopes': scopes,
        'token_saver': token_saver,
    }
    for key in CONFIG_KEYS:
        config_key = 'BYNDER_{}'.format(key.upper())
        value = os.environ.get(
            config_key, config['DEFAULT'].get(config_key)) or None
        if value:
            portal_config[key] = value

    use_token = FLOWS['token'].issubset(portal_config.keys())
    use_auth_code_flow = FLOWS['authorization_code'].issubset(
        portal_config.keys())
    use_client_credentials_flow = FLOWS['client_credentials'].issubset(
        portal_config.keys())

    if not any((use_token, use_auth_code_flow, use_client_credentials_flow)):
        raise Exception(
            'Missing required configuration, please make sure one ' +
            'of the following sets is configured: {}'.format(FLOWS.values()))

    if use_token:
        print('Access token passed, using arbitrary expiration of 60s')
        portal_config['token'] = {
            'token_type': 'bearer',
            'expires_in': 0,
            'scopes': scopes,
            'access_token': portal_config['access_token']
        }

    client = BynderClient(**portal_config)

    if use_auth_code_flow and not use_token:
        print('> Executing Authorization Code flow')
        print('> Generating authorization URL')
        print(client.get_authorization_url())

        code = input('Code: ')
        pp.pprint(client.fetch_token(code))

    if use_client_credentials_flow:
        print('> Executing Client Credentials flow')

    return client
