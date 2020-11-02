# Copyright 2017 Fortinet, Inc.
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
import json
import time

from common import singleton
from templates import fascomm as templates
from api_client import generic_request
from api_client import eventlet_request


LOG = logging.getLogger(__name__)

DEFAULT_HTTP_TIMEOUT = const.DEFAULT_HTTP_TIMEOUT
DEFAULT_RETRIES = const.DEFAULT_RETRIES
DEFAULT_REDIRECTS = const.DEFAULT_REDIRECTS
DEFAULT_CONTENT_TYPE = const.DEFAULT_HTTP_HEADERS['Content-Type']


@singleton.singleton
class FASCommApiClient(client.ApiClient):
    """The FAS Commercial API Client."""

    user_agent = 'FAS Python Commercial API Client'

    def __init__(self, api_providers, user=None, password=None,
                 client_id=None, client_secret=None,
                 key_file=None, cert_file=None, ca_file=None, ssl_sni=None,
                 concurrent_connections=base.DEFAULT_CONCURRENT_CONNECTIONS,
                 gen_timeout=base.GENERATION_ID_TIMEOUT,
                 use_https=True,
                 connect_timeout=base.DEFAULT_CONNECT_TIMEOUT,
                 http_timeout=DEFAULT_HTTP_TIMEOUT,
                 retries=DEFAULT_RETRIES,
                 redirects=DEFAULT_REDIRECTS,
                 auto_login=True):
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
        super(FASCommApiClient, self).__init__(
            api_providers, key_file=key_file,
            cert_file=cert_file, ca_file=ca_file, ssl_sni=ssl_sni,
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
        self._key_file = key_file
        self._cert_file = cert_file
        self._ca_file = ca_file
        # SSL server_name_indication
        self._ssl_sni = ssl_sni
        self._auto_login = auto_login
        self._template = templates
        self.client_id = client_id
        self.client_secret = client_secret

    def _login(self, conn=None, headers=None):
        """
        :param conn: Not use here
        :param headers: Not use here
        :return: return authenticated Header
        """

        print('execute login')

        g = eventlet_request.TokenRequestEventlet(
            self, self.client_id, self.client_secret, conn, headers)
        g.start()

        ret = g.join()

        if ret:
            if isinstance(ret, Exception):
                LOG.error("login error {}".format(ret))
                raise ret

            if ret.status != 201:
                LOG.error("login error {}".format(ret))
                raise Exception('Fail to fetch the token')

            ret_body = json.loads(ret.body)
            access_token = ret_body['access_token']

        return {'Authorization': 'Bearer {}'.format(access_token), 'Date': time.time()}

    def login_msg(self):

        return getattr(self._template, 'LOGIN')

    def auth_data(self, conn):
        # auth_data could be cookie or other fields with authentication
        # info in http headers.
        auth_data = None
        data = self._get_provider_data(conn)
        if data:
            auth_data = data[1]
            if auth_data:
                create_time = auth_data['Date']
                if time.time() - create_time > const.FTC_TOKEN_EXPIRE:
                    return None
        return auth_data

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

    def request_response(self, method, url, response, **kwargs):
        if response:
            response.body = self.request_response_body(response)
        return response
