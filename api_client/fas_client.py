# -*- coding: utf-8 -*-
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#

from oslo_log import log as logging

from . import base
from . import client
from . import constants as const
from . import eventlet_request
from .templates import fas as templates

LOG = logging.getLogger(__name__)

DEFAULT_HTTP_TIMEOUT = const.DEFAULT_HTTP_TIMEOUT
DEFAULT_RETRIES = const.DEFAULT_RETRIES
DEFAULT_REDIRECTS = const.DEFAULT_REDIRECTS


class FASApiClient(client.ApiClient):
    """The FAS API Client."""

    user_agent = 'FAS Python API Client'

    def __init__(self, api_providers, user=None, password=None,
                 key_file=None, cert_file=None, ca_file=None, ssl_sni=None,
                 concurrent_connections=base.DEFAULT_CONCURRENT_CONNECTIONS,
                 gen_timeout=base.GENERATION_ID_TIMEOUT,
                 use_https=True,
                 connect_timeout=base.DEFAULT_CONNECT_TIMEOUT,
                 http_timeout=DEFAULT_HTTP_TIMEOUT,
                 retries=DEFAULT_RETRIES,
                 redirects=DEFAULT_REDIRECTS,
                 auto_login=True,
                 headers=None,
                 singlethread=False):
        """
        Constructor. Adds the following:
        :param api_providers: a list of tuples of the form: (host, port,
            is_ssl)
        :param http_timeout: how long to wait before aborting an
            unresponsive controller (and allow for retries to another
            controller in the cluster)
        :param retries: the number of http/https request to retry.
        :param redirects: the number of concurrent connections.
        """
        super(FASApiClient, self).__init__(
            api_providers, key_file=key_file,
            cert_file=cert_file, ca_file=ca_file, ssl_sni=ssl_sni,
            concurrent_connections=concurrent_connections,
            gen_timeout=gen_timeout, use_https=use_https,
            connect_timeout=connect_timeout, http_timeout=http_timeout,
            retries=retries, redirects=redirects, auto_login=auto_login,
            headers=headers, singlethread=singlethread)

        self._request_timeout = http_timeout * retries
        self._http_timeout = http_timeout
        self._retries = retries
        self._redirects = redirects
        self._version = None
        self.message = {}
        self._key_file = key_file
        self._cert_file = cert_file
        self._ca_file = ca_file
        # SSL server_name_indication
        self._ssl_sni = ssl_sni
        self._auto_login = auto_login
        self._template = templates

    def _login(self, conn=None, headers=None):
        """
        :param conn: Not use here
        :param headers: Not use here
        :return: return authenticated Header
        """
        if self._ssl_sni:
            return {'Host': self._ssl_sni}
        return {}


class FASGenericApiClient(client.ApiClient):
    """The FAS General API Client."""

    user_agent = 'FAS Generic API Client'

    def __init__(self, api_providers, client_id=None, client_secret=None,
                 key_file=None, cert_file=None, ca_file=None, ssl_sni=None,
                 concurrent_connections=base.DEFAULT_CONCURRENT_CONNECTIONS,
                 gen_timeout=base.GENERATION_ID_TIMEOUT,
                 use_https=True,
                 connect_timeout=base.DEFAULT_CONNECT_TIMEOUT,
                 http_timeout=DEFAULT_HTTP_TIMEOUT,
                 retries=DEFAULT_RETRIES,
                 redirects=DEFAULT_REDIRECTS,
                 auto_login=True,
                 headers=None,
                 singlethread=False):
        """
        Constructor. Adds the following:
        :param api_providers: a list of tuples of the form: (host, port,
            is_ssl)
        :param http_timeout: how long to wait before aborting an
            unresponsive controller (and allow for retries to another
            controller in the cluster)
        :param retries: the number of http/https request to retry.
        :param redirects: the number of concurrent connections.
        """
        super(FASGenericApiClient, self).__init__(
            api_providers, key_file=key_file,
            cert_file=cert_file, ca_file=ca_file, ssl_sni=ssl_sni,
            concurrent_connections=concurrent_connections,
            gen_timeout=gen_timeout, use_https=use_https,
            connect_timeout=connect_timeout, http_timeout=http_timeout,
            retries=retries, redirects=redirects, auto_login=auto_login,
            headers=headers, singlethread=singlethread)

        self._request_timeout = http_timeout * retries
        self._http_timeout = http_timeout
        self._retries = retries
        self._redirects = redirects
        self._version = None
        self.message = {}
        self._client_id = client_id
        self._client_secret = client_secret
        self._key_file = key_file
        self._cert_file = cert_file
        self._ca_file = ca_file
        # SSL server_name_indication
        self._ssl_sni = ssl_sni
        self._auto_login = auto_login
        self._template = templates

    def auth_data(self, conn):
        # auth_data could be cookie or other fields with authentication
        # info in http headers.
        data = super().auth_data(conn)
        return {'Authorization': 'Bearer %s' % data} if data else data

    def _login(self, conn=None, headers=None):
        """ FAZ login method.
            FAZ need to get session before any request.
        :param conn: Not use here
        :param headers: Not use here
        :return: void
        """
        kwargs = {'client_id': self._client_id,
                  'client_secret': self._client_secret}
        message = self.render(getattr(self._template, 'LOGIN'), **kwargs)
        g = eventlet_request.EventletApiRequest(
            self, message['path'], method=message['method'],
            body=message['body'], headers=const.DEFAULT_HTTP_HEADERS,
            auto_login=self._auto_login, client_conn=conn)
        g.start()
        ret = g.join()
        if not ret:
            return None

        if (isinstance(ret, Exception) or
                201 != getattr(ret, 'status', None)):
            LOG.error('Login error "%s"', ret)
            raise ret

        response = self.request_response_body(ret)
        return response["access_token"]
