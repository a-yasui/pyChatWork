# coding: utf-8

from .api.Account import Account
from .api.Room    import Room
from .api import errors

import requests
import json


class pyChatWork:

    _headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'}

    def __init__ (self, key, api_base="https://api.chatwork.com/v1"):
        self.api_base = api_base
        self.account = Account(self)
        self.room    = Room(self)
        self._headers['X-ChatWorkToken'] = key

    def post(self, path, params):
        return self._request('post', path, params)

    def put(self, path, params):
        return self._request('put', path, params)

    def delete(self, path, params):
        return self._request('delete', path, params)

    def get(self, path, params={}):
        return self._request('get', path, params)

    def _request(self, method, path, params):
        try:
            r = requests.request(method, self.api_base + path,
                                 data = params,
                                 headers = self._headers)
        except requests.RequestException as exc:
            raise errors.ApiConnectionError(
                "Error while requesting API %s:%s" % (type(exc), exc),
                None, None, exc)
        return self._process_response(r)

    def _process_response(self, r):
        status = r.status_code
        try:
            data = r.json()
        except Exception as exc:
            raise errors.ApiConnectionError(
                "Error while parsing response JSON %s:%s\n%s" %
                (type(exc), exc, r.text),
                None, None, exc)

        if status >= 200 and status < 300:
            return data
        elif status == 400 or status == 404:
            error_info = data.get('error')
            raise errors.InvalidRequestError("Invalid path {1} / {0}".format(path, method), status, error_info)
        elif status == 401:
            error_info = data.get('error')
            raise errors.AuthenticationError(status, error_info)
        else:
            error_info = data.get('error')
            raise errors.ApiError(status, error_info)


