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

import base
import constants as const
import eventlet_client
import eventlet_request
import exceptions
from _i18n import _LE, _LW

LOG = logging.getLogger(__name__)

DEFAULT_HTTP_TIMEOUT = const.DEFAULT_HTTP_TIMEOUT
DEFAULT_RETRIES = const.DEFAULT_RETRIES
DEFAULT_REDIRECTS = const.DEFAULT_REDIRECTS
DEFAULT_USER_AGENT = const.DEFAULT_HTTP_HEADERS['User-Agent']
DEFAULT_CONTENT_TYPE = const.DEFAULT_HTTP_HEADERS['Content-Type']


class ApiClient(eventlet_client.EventletApiClient):
    """The FortiOS API Client."""

    user_agent = DEFAULT_USER_AGENT

    def __init__(self, api_providers, user=None, password=None,
                 key_file=None, cert_file=None, ca_file=None, ssl_sni=None,
                 concurrent_connections=base.DEFAULT_CONCURRENT_CONNECTIONS,
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
        super(ApiClient, self).__init__(
            api_providers, user, password, key_file=key_file,
            cert_file=cert_file, ca_file=ca_file, ssl_sni=ssl_sni,
            concurrent_connections=concurrent_connections,
            gen_timeout=gen_timeout, use_https=use_https,
            connect_timeout=connect_timeout)

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

    def _login(self, conn=None, headers=None):
        """ FortiAuthenticator use http basic auth, doesn't need to login,
           here reuse the name login to unify the API client process.
        :param conn: Not use here
        :param headers: Not use here
        :return: return authenticated Header
        """
        if self._ssl_sni:
            return {'Host': self._ssl_sni}
        return {}

    def request(self, opt, content_type=DEFAULT_CONTENT_TYPE, **message):
        """
        Issues request to controller.
        """
        self.message = self.render(getattr(self._template, opt),
                                   content_type=content_type, **message)
        method = self.message['method']
        url = self.message['path']
        body = self.message['body'] if 'body' in self.message else None
        g = eventlet_request.GenericRequestEventlet(
            self, method, url, body, content_type, self.user_agent,
            auto_login=self._auto_login,
            http_timeout=self._http_timeout,
            retries=self._retries, redirects=self._redirects)
        g.start()
        return self.request_response(method, url, g.join())

    def request_response(self, method, url, response):
        """
          response is a modified HTTPResponse object or None.
          response.read() will not work on response as the underlying library
          request_eventlet.ApiRequestEventlet has already called this
          method in order to extract the body and headers for processing.
          ApiRequestEventlet derived classes call .read() and
          .getheaders() on the HTTPResponse objects and store the results in
          the response object's .body and .headers data members for future
          access.
        """
        if response is None:
            # Timeout.
            LOG.error(_LE('Request timed out: %(method)s to %(url)s'),
                      {'method': method, 'url': url})
            raise exceptions.RequestTimeout()

        status = response.status
        LOG.debug("response.status = %(status)s", {'status': status})
        if status == 401:
            raise exceptions.UnAuthorizedRequest()
        # Fail-fast: Check for exception conditions and raise the
        # appropriate exceptions for known error codes.
        if status in [404]:
            LOG.warning(_LW("Resource not found. Response status: %(status)s, "
                            "response body: %(response.body)s"),
                        {'status': status, 'response.body': response.body})
            exceptions.ERROR_MAPPINGS[status](response)
        elif status in exceptions.ERROR_MAPPINGS:
            LOG.error(_LE("Received error code: %s"), status)
            LOG.error(_LE("Server Error Message: %s"), response.body)
            exceptions.ERROR_MAPPINGS[status](response)

        # Continue processing for non-error condition.
        if status != 200 and status != 201 and status != 204:
            LOG.error(_LE("%(method)s to %(url)s, unexpected response code: "
                          "%(status)d (content = '%(body)s')"),
                      {'method': method, 'url': url,
                       'status': response.status, 'body': response.body})
            return None
        return self.request_response_body(response)

    @staticmethod
    def request_response_body(response):
        if response and response.body:
            try:
                result = jsonutils.loads(response.body)
                LOG.debug("response.body = %(body)s", {'body': result})
                return result['objects'] if 'objects' in result else result
            except UnicodeDecodeError:
                LOG.debug("The following strings cannot be decoded with "
                          "'utf-8, trying 'ISO-8859-1' instead. %(body)s",
                          {'body': response.body})
                return jsonutils.loads(response.body, encoding='ISO-8859-1')
            except ValueError:
                LOG.info("Cannot decode response body with json, "
                         "return body directly '%(body)s'",
                         {'body': response.body})
                return response.body
            except Exception as e:
                LOG.error("json decode error %(e)s, the response '%(body)s'",
                          {'e': e.__class__, 'body': response.body})
                return response.body
        return response
