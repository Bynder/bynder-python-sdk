from bynder_sdk.version import VERSION

UA_HEADER = {
    'User-Agent': 'bynder-python-sdk/{}'.format(VERSION)
}


def api_endpoint_url(session, endpoint, is_fs_endpoint=False):
    if is_fs_endpoint:
        return 'https://{}{}'.format(session.bynder_domain, endpoint)
    return 'https://{}/api{}'.format(session.bynder_domain, endpoint)


def parse_json_for_response(response):
    try:
        return response.json()
    except ValueError:
        return None


class SessionMixin:
    def wrapped_request(self, func, endpoint, need_response_json=True,
                        is_fs_endpoint=False, *args,
                        **kwargs):
        endpoint = api_endpoint_url(self, endpoint,
                                    is_fs_endpoint=is_fs_endpoint)
        response = func(endpoint, *args, **kwargs)
        response.raise_for_status()
        if not need_response_json:
            return response
        return parse_json_for_response(response)

    def get(self, url, *args, **kwargs):
        return self.wrapped_request(super().get, url, *args, **kwargs)

    def post(self, url, need_response_json=True,
             is_fs_endpoint=False, *args, **kwargs):
        if url.startswith('https'):
            # Do not send the Authorization header to S3
            kwargs['headers'] = {'Authorization': None}
            return super().post(url, *args, **kwargs)
        return self.wrapped_request(super().post, url,
                                    need_response_json=need_response_json,
                                    is_fs_endpoint=is_fs_endpoint,
                                    *args,
                                    **kwargs)

    def put(self, url, *args, **kwargs):
        return self.wrapped_request(super().put, url, *args, **kwargs)

    def delete(self, url, *args, **kwargs):
        return self.wrapped_request(super().delete, url, *args, **kwargs)

    def _set_ua_header(self):
        self.headers.update(UA_HEADER)
