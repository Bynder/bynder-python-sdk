class Credentials:
    """ Token credentials to call the API.
    """
    def __init__(self, consumer_key, consumer_secret, token, token_secret):
        # Consumer key
        self._consumer_key = consumer_key

        # Consumer secret
        self._consumer_secret = consumer_secret

        # Access token key
        self._token = token

        # Access token secret
        self._token_secret = token_secret

        # Initial token key. Used when we want to reset credentials
        self._initial_token = token

        # Initial token secret. Used when we want to reset credentials
        self._initial_token_secret = token_secret

    @property
    def consumer_key(self):
        return self._consumer_key

    @property
    def consumer_secret(self):
        return self._consumer_secret

    @property
    def token(self):
        return self._token

    @property
    def token_secret(self):
        return self._token_secret

    def clear(self):
        """ Clears the access token key/secret.
        """
        self._token = None
        self._token_secret = None

    def reset(self):
        """ Resets access token key/secret to the initial ones.
        """
        self._token = self._initial_token
        self._token_secret = self._initial_token_secret

    def set(self, token, token_secret):
        """ Sets new access token key/secret.
        """
        self._token = token
        self._token_secret = token_secret
