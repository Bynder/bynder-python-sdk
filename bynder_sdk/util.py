from bynder_sdk.version import VERSION

UA_HEADER = {
    'User-Agent': 'bynder-python-sdk/{}'.format(VERSION)
}


def api_endpoint_url(session, endpoint):
    if endpoint.startswith('/v6') or endpoint.startswith('/v7'):
        return 'https://{}{}'.format(session.bynder_domain, endpoint)
    return 'https://{}/api{}'.format(session.bynder_domain, endpoint)


class SessionMixin:
    def wrapped_request(self, func, endpoint, *args, **kwargs):
        endpoint = api_endpoint_url(self, endpoint)
        response = func(endpoint, *args, **kwargs)
        response.raise_for_status()
        try:
            return response.json()
        except ValueError:
            return response

    def get(self, url, *args, **kwargs):
        return self.wrapped_request(super().get, url, *args, **kwargs)

    def post(self, url, *args, **kwargs):
        if url.startswith('https'):
            # Do not send the Authorization header to S3
            kwargs['headers'] = {'Authorization': None}
            return super().post(url, *args, **kwargs)
        return self.wrapped_request(super().post, url, *args, **kwargs)

    def put(self, url, *args, **kwargs):
        return self.wrapped_request(super().put, url, *args, **kwargs)

    def delete(self, url, *args, **kwargs):
        return self.wrapped_request(super().delete, url, *args, **kwargs)

    def _set_ua_header(self):
        self.headers.update(UA_HEADER)
