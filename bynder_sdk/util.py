from bynder_sdk.version import VERSION

UA_HEADER = {
    'User-Agent': f'bynder-python-sdk/{VERSION}'
}


def api_endpoint_url(session, endpoint):
    return f'https://{session.bynder_domain}/api{endpoint}'


def parse_json_for_response(response):
    try:
        return response.json()
    except ValueError:
        return None


class SessionMixin:
    def wrapped_request(self, func, endpoint, *args, **kwargs):
        endpoint = api_endpoint_url(self, endpoint)
        response = func(endpoint, *args, **kwargs)
        response.raise_for_status()

        return parse_json_for_response(response)

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
