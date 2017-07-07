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

import jinja2
from oslo_log import log as logging
from oslo_serialization import jsonutils

import base
import constants as const
import eventlet_client
import eventlet_request
import exceptions
from _i18n import _LE, _LW
from common import singleton
from templates import forticare as templates

LOG = logging.getLogger(__name__)

DEFAULT_HTTP_TIMEOUT = const.DEFAULT_HTTP_TIMEOUT
DEFAULT_RETRIES = const.DEFAULT_RETRIES
DEFAULT_REDIRECTS = const.DEFAULT_REDIRECTS
DEFAULT_HTTP_AUTH_SCH = const.HTTP_BASIC_AUTH_SCH


@singleton.singleton
class FortiCareApiClient(eventlet_client.EventletApiClient):
    """The FortiOS API Client."""

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
                 auth_sch=DEFAULT_HTTP_AUTH_SCH):
        '''Constructor. Adds the following:
        :param api_providers: a list of tuples of the form: (host, port,
            is_ssl)
        :param http_timeout: how long to wait before aborting an
            unresponsive controller (and allow for retries to another
            controller in the cluster)
        :param retries: the number of http/https request to retry.
        :param redirects: the number of concurrent connections.
        '''
        super(FortiCareApiClient, self).__init__(
            api_providers, user, password,
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
        self.key_file = key_file
        self.cert_file = cert_file
        self.ca_file = ca_file
        # SSL server_name_indication
        self.ssl_sni = ssl_sni
        self._auto_login = auto_login
        self._auth_sch = auth_sch

    @staticmethod
    def _render(template, **message):
        '''Render API message from it's template

        :param template: defined API message with essential params.
        :param message: It is a dictionary, included values of the params
                        for the template
        '''
        if not message:
            message = {}
        msg = jinja2.Template(template).render(**message)
        return jsonutils.loads(msg)

    def _login(self, conn=None, headers=None):
        """ FortiAuthenticator use http basic auth, doesn't need to login,
           here reuse the name login to unify the API client process.
        :param conn: Not use here
        :param headers: Not use here
        :return: return authenticated Header
        """
        return {'Authorization': self.format_auth_basic()}

    def request(self, opt, content_type="application/json", **message):
        '''Issues request to controller.'''
        import pdb;pdb.set_trace()
        self.message = self._render(getattr(templates, opt), **message)
        method = self.message['method']
        url = self.message['path']
        body = self.message['body'] if 'body' in self.message else None
        print "request.url = %s" % url
        print "request.method = %s" % method
        print "request.body = %s" % body
        g = eventlet_request.GenericRequestEventlet(
            self, method, url, body, content_type, auto_login=self._auto_login,
            http_timeout=self._http_timeout,
            retries=self._retries, redirects=self._redirects)
        g.start()
        response = g.join()

        # response is a modified HTTPResponse object or None.
        # response.read() will not work on response as the underlying library
        # request_eventlet.ApiRequestEventlet has already called this
        # method in order to extract the body and headers for processing.
        # ApiRequestEventlet derived classes call .read() and
        # .getheaders() on the HTTPResponse objects and store the results in
        # the response object's .body and .headers data members for future
        # access.

        if response is None:
            # Timeout.
            LOG.error(_LE('Request timed out: %(method)s to %(url)s'),
                      {'method': method, 'url': url})
            raise exceptions.RequestTimeout()

        status = response.status
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
        print "response.status = ", status
        if response.body:
            try:
                result = jsonutils.loads(response.body)
                print "response.body = ", result
                print ""
                return result['objects'] if 'objects' in result else result
            except UnicodeDecodeError:
                LOG.debug("The following strings cannot be decoded with "
                          "'utf-8, trying 'ISO-8859-1' instead. %(body)s",
                          {'body': response.body})
                return jsonutils.loads(response.body, encoding='ISO-8859-1')
            except Exception as e:
                LOG.error(_LE("Decode error, the response.body %(body)s"),
                          {'body': response.body})
                raise e
        else:
            print ""
            return None
