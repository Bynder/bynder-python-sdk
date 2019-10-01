from unittest import mock, TestCase

from bynder_sdk.oauth2 import (
    BynderOAuth2Session,
    api_endpoint_url,
    oauth2_url,
)


TEST_DOMAIN = 'test.getbynder.com'


class OAuth2Test(TestCase):
    def setUp(self):
        self.oauth2_session = BynderOAuth2Session(
            'test.getbynder.com',
            redirect_uri='https://test.com/',
            client_id='client_id',
            auto_refresh_kwargs={
                'client_id': 'client_id',
                'client_secret': 'client_secret'
            },
        )

    def test_oauth2_url(self):
        self.assertEqual(
            oauth2_url(TEST_DOMAIN, 'token'),
            'https://{}/v6/authentication/oauth2/token'.format(TEST_DOMAIN),
        )

    def test_api_endpoint_url(self):
        self.assertEqual(
            api_endpoint_url(self.oauth2_session, '/v4/users/'),
            'https://{}/api/v4/users/'.format(TEST_DOMAIN)
        )

    @mock.patch('requests_oauthlib.OAuth2Session.authorization_url')
    def test_authorization_url(self, mocked_func):
        self.oauth2_session.authorization_url()
        assert mocked_func.call_count == 1

    @mock.patch('requests_oauthlib.OAuth2Session.fetch_token')
    def test_fetch_token(self, mocked_func):
        self.oauth2_session.fetch_token('code')
        mocked_func.assert_called_with(
            oauth2_url(TEST_DOMAIN, 'token'),
            client_secret='client_secret',
            include_client_id=True,
            code='code',
        )
