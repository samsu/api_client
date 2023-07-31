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

from . import base
from . import constants as const
from . import client
from . import eventlet_request

from .common import utils
from .templates import faz as default_template

LOG = logging.getLogger(__name__)

DEFAULT_HTTP_TIMEOUT = const.DEFAULT_HTTP_TIMEOUT
DEFAULT_RETRIES = const.DEFAULT_RETRIES
DEFAULT_REDIRECTS = const.DEFAULT_REDIRECTS


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
                 redirects=DEFAULT_REDIRECTS, session=None,
                 auto_login=False, singlethread=False, **kwargs):
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

        self._url = "/jsonrpc"
        self._session=session
        self._method = "POST"
    
    def _login(self, conn=None, headers=None):
        """ FAZ login method.
            FAZ need to get session before any request.
        :param conn: Not use here
        :param headers: Not use here
        :return: void
        """
        if not self._session:
            body = self.render(
                getattr(self._template, 'LOGIN'), user=self._user,
                password=self._password
            )
            login_headers = {'Content-Type': 'application/json'}
            g = eventlet_request.EventletApiRequest(
                self, self._url, method='POST', body=body,
                headers=login_headers, auto_login=self._auto_login,
                client_conn=conn
            )
            g.start()
            ret = g.join()
            if ret:
                if isinstance(ret, Exception):
                    LOG.error('Login error "%s"', ret)
                    raise ret
                response = self.request_response_body(ret)
                self._session = response["session"]

    def request(self, opt, http_timeout=None, **message):
        """
        Issues request to controller.
        """
        self._login()
        message.update({'session': self._session})
        body = self.render(getattr(self._template, opt), **message)
        http_timeout = http_timeout or self._http_timeout
        g = eventlet_request.GenericRequestEventlet(
            self, self._method, self._url, body, const.DEFAULT_CONTENT_TYPE,
            self.user_agent, auto_login=self._auto_login,
            http_timeout=http_timeout,
            retries=self._retries, redirects=self._redirects,
            singlethread=self._singlethread)
        g.start()
        response = self.request_response(self._method, self._url, g.join())
        return response
