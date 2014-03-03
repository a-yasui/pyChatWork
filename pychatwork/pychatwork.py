# coding: utf-8

from .api.Account import Account
from .api.Room    import Room
from .api import errors

import logging
import requests
import json

## HTTP Debug Output if you wanna.
# import httplib
# httplib.HTTPConnection.debuglevel = 1
# logging.basicConfig() 
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True

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
        self._headers["Content-Type"] = "application/x-www-form-urlencoded"
        return self._request('POST', path, params)

    def put(self, path, params):
        self._headers["Content-Type"] = "application/x-www-form-urlencoded"
        return self._request('PUT', path, params)

    def delete(self, path, params):
        return self._request('DELETE', path, params)

    def get(self, path, params={}):
        return self._request('GET', path, params)

    def _request(self, method, path, params):
        try:
            r = requests.request(method, self.api_base + path,
                                 data = params,
                                 headers = self._headers)
            logging.warn("%s %s params:%s headers:%s", method, path, params, self._headers)
        except requests.RequestException as exc:
            raise errors.ApiConnectionError(
                "Error while requesting API %s:%s" % (type(exc), exc),
                None, None, exc)
        return self._process_response(r, self.api_base + path, method)

    def _process_response(self, r, path, method):
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
            raise errors.InvalidRequestError("Invalid path {1} / {0} => {2}".format(path, method, data), status, error_info)
        elif status == 401:
            error_info = data.get('error')
            raise errors.AuthenticationError(status, error_info)
        else:
            error_info = data.get('error')
            raise errors.ApiError(status, error_info)


