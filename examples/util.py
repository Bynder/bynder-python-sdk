import os
import pprint
from configparser import ConfigParser

pp = pprint.PrettyPrinter()

try:
    from bynder_sdk import BynderClient
except ModuleNotFoundError as exc:
    raise RuntimeError(
        'Please run pip install . before running the examples') from exc

TOKEN_ARGS = {'domain', 'access_token'}
AUTH_CODE_FLOW_ARGS = {
    'domain', 'client_id', 'client_secret', 'redirect_uri'}


def get_client(scopes):
    print('> Creating instance of BynderClient and go through ' +
          'authorization code flow if necessary.')
    config = ConfigParser()
    config.read(
        os.path.join(os.path.dirname(__file__), 'config.ini')
    )

    # Build a dictionary based on the config file and environment variables
    portal_config = {}
    for key in TOKEN_ARGS | AUTH_CODE_FLOW_ARGS:
        config_key = 'BYNDER_{}'.format(key.upper())
        value = os.environ.get(
            config_key, config['DEFAULT'].get(config_key)) or None
        if value:
            portal_config[key] = value

    use_token = TOKEN_ARGS.issubset(portal_config.keys())
    use_auth_code_flow = AUTH_CODE_FLOW_ARGS.issubset(portal_config.keys())

    if not use_token and not use_auth_code_flow:
        raise Exception(
            'Missing required configuration, please make sure ' +
            'one of the following sets is ' +
            'configured: {} or {}'.format(TOKEN_ARGS, AUTH_CODE_FLOW_ARGS))

    if use_token:
        print('Access token passed, using arbitrary expiration of 60s')
        portal_config['token'] = {
            'token_type': 'bearer',
            'expires_in': 60,
            'scopes': scopes,
            'access_token': portal_config['access_token']
        }

    def token_saver(token):
        """ This function will be called by oauthlib-requests when a new
        token is retrieved, either after the initial login or refreshing an
        existing token. """
        print('New token received:')
        pp.pprint(token)

    client = BynderClient(
        **portal_config, scopes=scopes, token_saver=token_saver)

    if not use_token and use_auth_code_flow:
        print('> Generating authorization URL')
        print(client.get_authorization_url())

        code = input('Code: ')
        pp.pprint(client.fetch_token(code))

    return client
