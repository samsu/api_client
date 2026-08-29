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
from . import constants as const
from . import client
from .templates import fortigate as templates

LOG = logging.getLogger(__name__)

DEFAULT_HTTP_TIMEOUT = const.DEFAULT_HTTP_TIMEOUT
DEFAULT_RETRIES = const.DEFAULT_RETRIES
DEFAULT_REDIRECTS = const.DEFAULT_REDIRECTS


class ScimApiClient(client.ApiClient):
    """The SCIM API Client for managing SCIM server communications."""

    user_agent = 'SCIM Python API Client'

    def __init__(
            self, api_providers, user=None, password=None,
            key_file=None, cert_file=None, ca_file=None, ssl_sni=None,
            concurrent_connections=base.DEFAULT_CONCURRENT_CONNECTIONS,
            gen_timeout=base.GENERATION_ID_TIMEOUT,
            use_https=True,
            connect_timeout=base.DEFAULT_CONNECT_TIMEOUT,
            http_timeout=DEFAULT_HTTP_TIMEOUT,
            retries=DEFAULT_RETRIES,
            redirects=DEFAULT_REDIRECTS,
            auto_login=False, singlethread=False,
            bearer_token=None
            ):
        """Constructor. Adds the following:
        :param api_providers: a list of tuples of the form: (host, port,
            is_ssl)
        :param bearer_token: OAuth Bearer token for SCIM authentication
        :param http_timeout: how long to wait before aborting an
            unresponsive controller (and allow for retries to another
            controller in the cluster)
        :param retries: the number of http/https request to retry.
        :param redirects: the number of concurrent connections.
        """
        super(ScimApiClient, self).__init__(
            api_providers, user=user, password=password, key_file=key_file,
            cert_file=cert_file, ca_file=ca_file, ssl_sni=ssl_sni,
            verify_peer=bool(ca_file),
            concurrent_connections=concurrent_connections,
            gen_timeout=gen_timeout, use_https=use_https,
            connect_timeout=connect_timeout, http_timeout=http_timeout,
            retries=retries, redirects=redirects, auto_login=auto_login,
            singlethread=singlethread
        )

        self._request_timeout = http_timeout * retries
        self._http_timeout = http_timeout
        self._retries = retries
        self._redirects = redirects
        self._version = None
        self.message = {}
        self._key_file = key_file
        self._cert_file = cert_file
        self._ca_file = ca_file
        self._ssl_sni = ssl_sni
        self._auto_login = auto_login
        self._bearer_token = bearer_token
        self._template = templates

    def _login(self, conn=None, headers=None):
        """
        SCIM authentication using Bearer token
        :param conn: Not use here
        :param headers: Not use here
        :return: return authenticated Header
        """
        auth_headers = {}

        if self._bearer_token:
            auth_headers['Authorization'] = f'Bearer {self._bearer_token}'

        # Add SCIM-specific headers
        auth_headers.update(
            {
                'Content-Type': 'application/scim+json',
                'Accept': 'application/scim+json'
            }
        )

        return auth_headers
