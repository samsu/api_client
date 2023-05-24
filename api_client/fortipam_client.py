# Copyright 2015 Fortinet, Inc.
#
# All Rights Reserved
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#

import re
from oslo_log import log as logging

from . import base
from . import client
from . import constants as const
from . import eventlet_request
from . import exceptions
from .templates import fortipam as templates

LOG = logging.getLogger(__name__)

DEFAULT_HTTP_TIMEOUT = const.DEFAULT_HTTP_TIMEOUT * 20
DEFAULT_RETRIES = 3
DEFAULT_REDIRECTS = 1
DEFAULT_CONCURRENT_CONNECTIONS = base.DEFAULT_CONCURRENT_CONNECTIONS
DEFAULT_CONTENT_TYPE = const.DEFAULT_HTTP_HEADERS['Content-Type']


class FortiPAMApiClient(client.ApiClient):
    """The FortiOS API Client."""

    user_agent = 'FortiPAM Python API Client'

    def __init__(self, api_providers, user=None, password=None,
                 key_file=None, cert_file=None, ca_file=None, ssl_sni=None,
                 verify_peer=False,
                 concurrent_connections=DEFAULT_CONCURRENT_CONNECTIONS,
                 gen_timeout=base.GENERATION_ID_TIMEOUT,
                 use_https=True,
                 connect_timeout=base.DEFAULT_CONNECT_TIMEOUT,
                 http_timeout=DEFAULT_HTTP_TIMEOUT,
                 retries=DEFAULT_RETRIES,
                 redirects=10,
                 auto_login=True,
                 singlethread=False):
        '''Constructor. Adds the following:
        :param api_providers: a list of tuples of the form: (host, port,
            is_ssl)
        :param http_timeout: how long to wait before aborting an
            unresponsive controller (and allow for retries to another
            controller in the cluster)
        :param retries: the number of http/https request to retry.
        :param redirects: the number of concurrent connections.
        '''
        super(FortiPAMApiClient, self).__init__(
            api_providers, user, password, key_file=key_file,
            verify_peer=verify_peer,
            cert_file=cert_file, ca_file=ca_file, ssl_sni=ssl_sni,
            concurrent_connections=concurrent_connections,
            gen_timeout=gen_timeout, use_https=use_https,
            connect_timeout=connect_timeout, http_timeout=http_timeout,
            retries=retries, redirects=redirects, auto_login=auto_login,
            singlethread=singlethread)

        self._request_timeout = http_timeout * retries
        self._http_timeout = http_timeout
        self._retries = retries
        self._redirects = redirects
        self._version = None
        self.message = {}
        self._user = user
        self._password = password
        self._key_file = key_file
        self._cert_file = cert_file
        self._ca_file = ca_file
        # SSL server_name_indication
        self._ssl_sni = ssl_sni
        self._auto_login = auto_login
        self._template = templates

    @staticmethod
    def parse_headers_cookie(headers):
        cookies = ''
        path = ''
        for key, value in headers:
            if key.lower() == 'set-cookie':
                cookie = value.split(';')[0]
                parse_cookie = re.search(
                    r"(?P<cookie_name>[^=]+)=(?P<cookie_value>[^;]+)(?:;|$)",
                    cookie
                )
                if parse_cookie:
                    # Skip cookie with value 0%260
                    if parse_cookie.group('cookie_value') != '"0%260"':
                        cookies += f'{cookie};'
            elif key.lower() == 'location':
                path = value
        return cookies, path

    def _login(self, conn=None, headers=None):
        """ FortiPAM login method. FortiPAM need to use login form to
            get x-csrf-token before any request.
        :param conn: Not use here
        :param headers: Not use here
        :return: return authenticated Header
        """
        cookies = ''
        message = self.render(
            getattr(self._template, 'LOGIN'), username=self._user,
            password=self._password
        )
        login_headers = {'Content-Type': 'text/plain'}
        g = eventlet_request.EventletApiRequest(
            self, message['path'], message['method'], message['body'],
            login_headers, auto_login=False, client_conn=conn
        )
        g.start()
        ret = g.join()
        if ret:
            if isinstance(ret, Exception):
                LOG.error('Login error "%s"', ret)
                raise ret
            res_headers = ret.headers
            cookie, path = self.parse_headers_cookie(res_headers)
            cookies += cookie
            if not path:
                raise exceptions.UnAuthorizedRequest()
        redirect_message = self.render(
            getattr(self._template, 'REDIRECT'), path=path)
        g = eventlet_request.EventletApiRequest(
            self, redirect_message['path'], redirect_message['method'],
            redirect_message.get('body', None), {'Cookie': cookies},
            auto_login=False, client_conn=conn
        )
        g.start()
        ret = g.join()
        if ret:
            if isinstance(ret, Exception):
                LOG.error('Login error "%s"', ret)
                raise ret
        redirect_headers = ret.headers
        cookie, _ = self.parse_headers_cookie(redirect_headers)
        cookies += cookie
        if cookies and 'ccsrftoken' in cookies:
            LOG.debug('Login success, saving cookies: %s', cookies)
            return self.format_cookie(cookies)
        else:
            LOG.error('Login failed, no cookies found')
            raise exceptions.UnAuthorizedRequest()

    def request_response(self, method, url, response, **kwargs):
        if response is None:
            # Timeout.
            LOG.error('Request timed out: %(method)s to %(url)s',
                      {'method': method, 'url': url})
            raise exceptions.RequestTimeout()
        if response:
            response.body = self.request_response_body(response)
        return response
