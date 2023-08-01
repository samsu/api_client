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
from oslo_serialization import jsonutils

from . import base
from . import client
from . import constants as const
from . import eventlet_request
from .common import utils
from .templates import faz as default_template

LOG = logging.getLogger(__name__)

DEFAULT_HTTP_TIMEOUT = const.DEFAULT_HTTP_TIMEOUT
DEFAULT_RETRIES = 0
DEFAULT_REDIRECTS = const.DEFAULT_REDIRECTS
SESSION_EXPIRE_CODE = -11


class FortiAnalyzerApiClient(client.ApiClient):
    """The FortiOS API Client."""

    user_agent = 'FortiAnalyzer JSON-RPC API Client'

    def __init__(self, api_providers, template=None, user=None, password=None,
                 key_file=None, cert_file=None, ca_file=None, ssl_sni=None,
                 concurrent_connections=base.DEFAULT_CONCURRENT_CONNECTIONS,
                 gen_timeout=base.GENERATION_ID_TIMEOUT,
                 use_https=True,
                 connect_timeout=base.DEFAULT_CONNECT_TIMEOUT,
                 http_timeout=DEFAULT_HTTP_TIMEOUT,
                 retries=DEFAULT_RETRIES,
                 redirects=DEFAULT_REDIRECTS,
                 auto_login=True, singlethread=False):
        """Constructor. Adds the following:
        :param api_providers: a list of tuples of the form: (host, port,
            is_ssl)
        :param http_timeout: how long to wait before aborting an
            unresponsive controller (and allow for retries to another
            controller in the cluster)
        :param retries: the number of http/https request to retry.
        :param redirects: the number of concurrent connections.
        """
        super(FortiAnalyzerApiClient, self).__init__(
            api_providers, user=user, password=password, key_file=key_file,
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
        self._key_file = key_file
        self._cert_file = cert_file
        self._ca_file = ca_file
        # SSL server_name_indication
        self._ssl_sni = ssl_sni
        self._auto_login = auto_login
        if template:
            path, files = utils.get_module_files('/templates')
            if not template.endswith('.py'):
                template = '.'.join([template, 'py'])

            if template in files:
                self._template = utils.import_file_module(path, template)
            else:
                raise EnvironmentError(
                    "Cannot find the template file {t}".format(t=template))
        else:
            self._template = default_template

    def set_auth_data(self, conn, session=None):
        """ Set authenticate data
        :param conn: conn parameters
        :param session:
        :return:
        """
        data = self._get_provider_data(conn)
        print("## set_auth_data() data = ", data)
        if data:
            self._set_provider_data(conn, (data[0], session))

    def apply_auth_data(self, conn, headers, body):
        session = self.auth_data(conn)
        if session:
            body.update({'session': session})
        return headers, body

    @staticmethod
    def auth_required(response):
        body = None
        content_type = response.content_type or ''
        if const.DEFAULT_CONTENT_TYPE in content_type and response.body:
            body = jsonutils.loads(response.body)

        if not response or not isinstance(body, dict):
            return True

        if body['result'][0]['status']['code'] == SESSION_EXPIRE_CODE:
            return True
        return False

    def _login(self, conn=None, headers=None):
        """ FAZ login method.
            FAZ need to get session before any request.
        :param conn: Not use here
        :param headers: Not use here
        :return: void
        """
        kwargs = {'user': self._user, 'password': self._password}
        message = self.render(getattr(self._template, 'LOGIN'), **kwargs)

        g = eventlet_request.EventletApiRequest(
            self, message['path'], method=message['method'],
            body=message['body'], headers=const.DEFAULT_HTTP_HEADERS,
            auto_login=self._auto_login, client_conn=conn)
        g.start()
        ret = g.join()
        if ret:
            if isinstance(ret, Exception):
                LOG.error('Login error "%s"', ret)
                raise ret
            response = self.request_response_body(ret)
            return response["session"]
