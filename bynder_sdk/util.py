def api_endpoint_url(session, endpoint):
    return 'https://{}/api{}'.format(session.bynder_domain, endpoint)


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

    def get(self, endpoint, *args, **kwargs):
        return self.wrapped_request(super().get, endpoint, *args, **kwargs)

    def post(self, endpoint, *args, **kwargs):
        if endpoint.startswith('https'):
            return super().post(endpoint, *args, **kwargs)
        return self.wrapped_request(super().post, endpoint, *args, **kwargs)

    def put(self, endpoint, *args, **kwargs):
        return self.wrapped_request(super().put, endpoint, *args, **kwargs)

    def delete(self, endpoint, *args, **kwargs):
        return self.wrapped_request(super().delete, endpoint, *args, **kwargs)
