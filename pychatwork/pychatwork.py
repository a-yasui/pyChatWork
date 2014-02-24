# coding: utf-8

from .api.Account import Account

import requests
import json


class pyChatWork:

    _headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'}

    def __init__ (self, key, api_base="https://api.chatwork.com/v1"):
        self.api_base = api_base
        self.account = Account(self)
        self._headers['X-ChatWorkToken'] = key

    def post(self, path, params):
        return self._request('post', path, params)

    def get(self, path, params={}):
        return self._request('get', path, params)

    def _request(self, method, path, params):
        try:
            r = requests.request(method, self.api_base + path,
                                 data = json.dumps(params),
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
        error_info = data.get('error')

        if status >= 200 and status < 300:
            return data
        elif status == 400 or status == 404:
            raise errors.InvalidRequestError(status, error_info)
        elif status == 401:
            raise errors.AuthenticationError(status, error_info)
        elif status == 402:
            raise errors.CardError(status, error_info)
        else:
            raise errors.ApiError(status, error_info)


