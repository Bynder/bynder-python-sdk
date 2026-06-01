from unittest import mock, TestCase

from bynder_sdk.oauth2 import BynderOAuth2Session, oauth2_url
from bynder_sdk.util import api_endpoint_url, UA_HEADER


TEST_DOMAIN = 'test.getbynder.com'


class OAuth2Test(TestCase):
    def setUp(self):
        self.session = BynderOAuth2Session(
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
            f'https://{TEST_DOMAIN}/v6/authentication/oauth2/token',
        )

    def test_api_endpoint_url(self):
        self.assertEqual(
            api_endpoint_url(self.session, '/v4/users/'),
            f'https://{TEST_DOMAIN}/api/v4/users/'
        )

    @mock.patch('bynder_sdk.oauth2.random.choice', return_value='a')
    @mock.patch('requests_oauthlib.OAuth2Session.authorization_url')
    def test_authorization_url(self, mocked_auth_url, mocked_choice):
        self.session.authorization_url()
        mocked_auth_url.assert_called_once_with(
            oauth2_url(TEST_DOMAIN, 'auth'),
            state='aaaaaaaa'
        )

    @mock.patch('requests_oauthlib.OAuth2Session.fetch_token')
    def test_fetch_token(self, mocked_func):
        self.session.fetch_token('code')
        mocked_func.assert_called_with(
            oauth2_url(TEST_DOMAIN, 'token'),
            client_secret='client_secret',
            include_client_id=True,
            code='code',
        )

    def test_user_agent_header(self):
        # The UA header is contained within the session headers
        assert UA_HEADER.items() <= self.session.headers.items()

    def test_oauth2_url_auth_endpoint(self):
        self.assertEqual(
            oauth2_url(TEST_DOMAIN, 'auth'),
            f'https://{TEST_DOMAIN}/v6/authentication/oauth2/auth',
        )

    def test_auto_refresh_url_set_on_init(self):
        self.assertEqual(
            self.session.auto_refresh_url,
            oauth2_url(TEST_DOMAIN, 'token'),
        )

    @mock.patch('bynder_sdk.util.SessionMixin.post')
    def test_post_https_url_withholds_token(self, mocked_post):
        self.session.post('https://example.com/api')
        mocked_post.assert_called_once_with(
            'https://example.com/api',
            withhold_token=True,
        )

    @mock.patch('bynder_sdk.util.SessionMixin.post')
    def test_post_http_url_does_not_withhold_token(self, mocked_post):
        self.session.post('http://example.com/api')
        mocked_post.assert_called_once_with('http://example.com/api')
