from unittest import mock, TestCase

from bynder_sdk.oauth2 import (
    api_endpoint_url,
    BynderOAuth2Session,
    oauth2_url,
    UA_HEADER,
)


TEST_DOMAIN = 'test.getbynder.com'


class OAuth2Test(TestCase):
    def setUp(self):
        self.session = BynderOAuth2Session(
            TEST_DOMAIN,
            redirect_uri='https://test.com/',
            client_id='client_id',
            client_secret='client_secret',
            scope=('asset:read', 'asset:write'),
        )

    def test_oauth2_url(self):
        self.assertEqual(
            oauth2_url(TEST_DOMAIN, 'token'),
            'https://{}/v6/authentication/oauth2/token'.format(TEST_DOMAIN),
        )

    def test_api_endpoint_url(self):
        self.assertEqual(
            api_endpoint_url(self.session, '/v4/users/'),
            'https://{}/api/v4/users/'.format(TEST_DOMAIN)
        )

        self.assertEqual(
            api_endpoint_url(self.session, '/v6/resource/'),
            'https://{}/v6/resource/'.format(TEST_DOMAIN)
        )

    @mock.patch('requests_oauthlib.OAuth2Session.authorization_url')
    def test_authorization_url(self, mocked_func):
        self.session.authorization_url()
        assert mocked_func.call_count == 1

    @mock.patch('requests_oauthlib.OAuth2Session.fetch_token')
    def test_fetch_token(self, mocked_func):
        self.session.fetch_token('code')
        mocked_func.assert_called_with(
            oauth2_url(TEST_DOMAIN, 'token'),
            client_secret='client_secret',
            scope=('asset:read', 'asset:write'),
            code='code',
        )

    def test_fetch_token_without_code_error(self):
        with self.assertRaises(ValueError):
            self.session.fetch_token()

    def test_passing_token(self):
        session = BynderOAuth2Session(
            TEST_DOMAIN,
            redirect_uri='https://test.com/',
            client_id='client_id',
            client_secret='client_secret',
            scope=('asset:read', 'asset:write'),
            token={'access_token': 'TOKEN'})

        self.assertEqual(session.authorized, True)

    @mock.patch('requests_oauthlib.OAuth2Session.fetch_token')
    @mock.patch('requests_oauthlib.OAuth2Session.request')
    def test_client_credentials_setup(self, fetch_token_mock, request_mock):
        session = BynderOAuth2Session(
            TEST_DOMAIN,
            client_id='client_id',
            client_secret='client_secret',
            scope=('asset:read', 'asset:write'),
            token={'access_token': 'TOKEN'})

        self.assertIsInstance(session, BynderOAuth2Session)

        with self.assertRaises(Warning):
            session.authorization_url()

        session.request('GET', 'test')
        self.assertEqual(fetch_token_mock.called, True)

    @mock.patch('requests_oauthlib.OAuth2Session.refresh_token')
    def test_refresh_credentials_passed(self, mock):
        token_endpoint = oauth2_url(TEST_DOMAIN, 'token')
        self.session.refresh_token(token_endpoint)

        mock.assert_called_with(
            token_endpoint, auth=('client_id', 'client_secret'))

    def test_user_agent_header(self):
        # The UA header is contained within the session headers
        assert UA_HEADER.items() <= self.session.headers.items()
