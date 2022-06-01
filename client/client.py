#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""pyierdYLIARD - Kraken Exchange API client.

This is a REST API client module which allows you to query the API endpoints of
the Kraken exchange. It can make public and private domain queries. In case of
private queries an API key is required. The key can be loaded from a file or
provided as a string.

https://docs.kraken.com/rest/
https://github.com/0x0100F/pyierd
"""


import base64
import hashlib
import hmac
import requests
import urllib.parse
import time


from . import version


__author__ = "0x0100F"
__version__ = version.__version__
__license__ = "Apache-2.0"


# ...
class Client(object):

    # ...
    def __init__(self, key='', secret=''):
        self.key = key
        self.secret = secret
        self.uri = 'https://api.kraken.com'
        self.apiversion = '0'
        self.session = requests.Session()
        self.session.headers.update(
            {'User-Agent': 'pyierd/' + version.__version__ +
             ' (+' + version.__url__ + ')'})
        self.response = None
        self._json_options = {}
        return

    # ...
    def load_key(self, keyfile):
        with open(keyfile, 'r') as f:
            self.key = f.readline().strip()
            self.secret = f.readline().strip()
        return

    # ...
    def json_options(self, **kwargs):
        self._json_options = kwargs
        return self

    # ...
    def query_public(self, endpoint, data=None, timeout=None):
        if data is None:
            data = {}
        return self._query(
            '/' + self.apiversion + '/public/' + endpoint, data,
            timeout=timeout)

    # ...
    def query_private(self, endpoint, data=None, timeout=None):
        if data is None:
            data = {}
        if not self.key or not self.secret:
            raise Exception('API key and secret required. Use `load_key` ' +
                            'method with the client.')
        data['nonce'] = self._nonce()
        url_path = '/' + self.apiversion + '/private/' + endpoint
        headers = {
            'API-Key': self.key,
            'API-Sign': self._sign(url_path, data)
        }
        return self._query(url_path, data, headers, timeout=timeout)

    # ...
    def close(self):
        self.session.close()
        return

    # ...
    def _nonce(self):
        return str(int(time.time() * 1000))

    # ...
    def _sign(self, endpoint, data):
        postdata = urllib.parse.urlencode(data)
        encoded = (str(data['nonce']) + postdata).encode()
        message = endpoint.encode() + hashlib.sha256(encoded).digest()
        mac = hmac.new(base64.b64decode(self.secret), message, hashlib.sha512)
        sigdigest = base64.b64encode(mac.digest())
        return sigdigest.decode()

    # ...
    def _query(self, endpoint, data, headers=None, timeout=None):
        if headers is None:
            headers = {}
        try:
            self.response = self.session.post(
                self.uri + endpoint, data=data, headers=headers,
                timeout=timeout)
            if self.response.status_code not in (200, 201, 202):
                self.response.raise_for_status()
            return self.response.json(**self._json_options)
        except requests.exceptions.RequestException as e:
            self.response = None
            raise e
