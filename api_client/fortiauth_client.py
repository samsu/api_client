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

from oslo_log import log as logging

import base
import constants as const
import client

import generic_request
from templates import fortiauth as templates

LOG = logging.getLogger(__name__)

DEFAULT_HTTP_TIMEOUT = const.DEFAULT_HTTP_TIMEOUT * 20
DEFAULT_RETRIES = 0
DEFAULT_REDIRECTS = 1
DEFAULT_CONCURRENT_CONNECTIONS = base.DEFAULT_CONCURRENT_CONNECTIONS
DEFAULT_CONTENT_TYPE = const.DEFAULT_HTTP_HEADERS['Content-Type']


class FortiAuthApiClient(client.ApiClient):
    """The FortiOS API Client."""

    user_agent = 'FortiAuth Python API Client'

    def __init__(self, api_providers, user, password,
                 concurrent_connections=DEFAULT_CONCURRENT_CONNECTIONS,
                 gen_timeout=base.GENERATION_ID_TIMEOUT,
                 use_https=True,
                 connect_timeout=base.DEFAULT_CONNECT_TIMEOUT,
                 http_timeout=DEFAULT_HTTP_TIMEOUT,
                 retries=DEFAULT_RETRIES,
                 redirects=DEFAULT_REDIRECTS,
                 auto_login=True):
        '''Constructor. Adds the following:
        :param api_providers: a list of tuples of the form: (host, port,
            is_ssl)
        :param http_timeout: how long to wait before aborting an
            unresponsive controller (and allow for retries to another
            controller in the cluster)
        :param retries: the number of http/https request to retry.
        :param redirects: the number of concurrent connections.
        '''
        super(FortiAuthApiClient, self).__init__(
            api_providers, user, password,
            concurrent_connections=concurrent_connections,
            gen_timeout=gen_timeout, use_https=use_https,
            connect_timeout=connect_timeout, http_timeout=http_timeout,
            retries=retries, redirects=redirects, auto_login=auto_login)

        self._request_timeout = http_timeout * retries
        self._http_timeout = http_timeout
        self._retries = retries
        self._redirects = redirects
        self._version = None
        self.message = {}
        self._user = user
        self._password = password
        self._auto_login = auto_login
        self._template = templates

    def _login(self, conn=None, headers=None):
        """ FortiAuthenticator use http basic auth, doesn't need to login,
           here reuse the name login to unify the API client process.
        :param conn: Not use here
        :param headers: Not use here
        :return: return authenticated Header
        """
        return {'Authorization': self.format_auth_basic()}

    def request(self, opt, content_type=DEFAULT_CONTENT_TYPE, **message):
        """
        Issues request to controller.
        """
        self.message = self.render(getattr(self._template, opt),
                                   content_type=content_type, **message)
        method = self.message['method']
        url = self.message['path']
        body = self.message['body'] if 'body' in self.message else None
        g = generic_request.GenericRequest(
            self, method, url, body, content_type, self.user_agent,
            auto_login=self._auto_login,
            http_timeout=self._http_timeout,
            retries=self._retries, redirects=self._redirects)
        response = g.start()
        return self.request_response(method, url, response)

    def request_response(self, method, url, response):
        if response:
            response.body = self.request_response_body(response)
        return response
