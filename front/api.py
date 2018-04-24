import requests

from front import exceptions


class API(object):
    base_url = 'https://api2.frontapp.com/'

    def __init__(self):
        self.jwt_key = None

    def set_key(self, key):
        self.jwt_key = key

    @property
    def _headers(self):
        return {
            'Authorization': 'Bearer {}'.format(self.jwt_key),
            'Content-Type': 'application/json',
        }

    def get(self, endpoint, params=None, **kwargs):
        return self._request('get', endpoint, params=params, **kwargs)

    def post(self, endpoint, data=None, json=None, **kwargs):
        return self._request('post', endpoint, data=data, json=json, **kwargs)

    def patch(self, endpoint, data=None, json=None, **kwargs):
        return self._request('patch', endpoint, data=data, json=json, **kwargs)

    def delete(self, endpoint, data=None, json=None, **kwargs):
        return self._request('delete', endpoint, data=data, json=json, **kwargs)

    def _request(self, method, endpoint, **kwargs):
        if self.jwt_key is None:
            raise exceptions.AuthenticationError(
                '`front.set_api_key` must be called before making api calls'
            )

        kwargs.setdefault('headers', {})
        kwargs['headers'].update(self._headers)

        url = '{}{}'.format(self.base_url, endpoint)

        if kwargs.pop('raw_url', False):
            url = endpoint

        response = requests.request(
            method=method,
            url=url,
            **kwargs
        )
        response.raise_for_status()
        if response.content:
            return response.json()
        else:
            return None


client = API()


def set_api_key(key):
    client.set_key(key)
