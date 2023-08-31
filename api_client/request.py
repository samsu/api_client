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

import abc
import copy

import eventlet

try:
    import httplib as httpclient
except ImportError:
    from http import client as httpclient
import time

from oslo_log import log as logging
from oslo_serialization import jsonutils
from oslo_utils import excutils
import six
import six.moves.urllib.parse as urlparse

from ._i18n import _, _LI, _LW
from .common import utils
from . import constants as const
from . import exceptions as ex

LOG = logging.getLogger(__name__)

DEFAULT_HTTP_TIMEOUT = const.DEFAULT_HTTP_TIMEOUT
DEFAULT_RETRIES = const.DEFAULT_RETRIES
DEFAULT_REDIRECTS = const.DEFAULT_REDIRECTS
DEFAULT_API_REQUEST_POOL_SIZE = const.DEFAULT_API_REQUEST_POOL_SIZE
DEFAULT_MAXIMUM_REQUEST_ID = const.DEFAULT_MAXIMUM_REQUEST_ID
DOWNLOAD_TIMEOUT = const.DOWNLOAD_TIMEOUT
DEFAULT_CONTENT_TYPE = const.DEFAULT_HTTP_HEADERS['Content-Type']


@six.add_metaclass(abc.ABCMeta)
class ApiRequest(object):
    """An abstract baseclass for all ApiRequest implementations.

    This defines the interface and property structure for both eventlet and
    gevent-based ApiRequest classes.
    """

    # List of allowed status codes.
    ALLOWED_STATUS_CODES = [
        200,
        201,
        204,
        301,
        302,
        400,
        401,
        403,
        404,
        407,
        409,
        500,
        503
    ]

    @abc.abstractmethod
    def start(self):
        pass

    @abc.abstractmethod
    def join(self):
        pass

    def get_conn(self):
        conn = self._client_conn or \
               self._api_client.acquire_connection(self._auto_login,
                                                   copy.copy(self._headers),
                                                   rid=self._rid())
        return conn

    def _issue_request(self):
        """Issue a request to a provider."""
        conn = self.get_conn()
        if conn is None:
            error = Exception(_("No API connections available"))
            self._request_error = error
            return error

        url = self._url
        # LOG.debug("[%(rid)d] Issuing - request url: %(conn)s, body: %(body)s",
        #           {'rid': self._rid(), 'conn': self._request_str(conn, url),
        #            'body': self._body})
        issued_time = time.time()
        is_conn_error = False
        is_conn_service_unavail = False
        response = None
        try:
            redirects = 0
            while redirects <= self._redirects:
                # Update connection with user specified request timeout,
                # the connect timeout is usually smaller so we only set
                # the request timeout after a connection is established
                if conn.sock is None:
                    conn.connect()
                    conn.sock.settimeout(self._http_timeout)
                elif conn.sock.gettimeout() != self._http_timeout:
                    conn.sock.settimeout(self._http_timeout)

                headers = copy.copy(self._headers)
                body = self._body
                auth = self._api_client.auth_data(conn)

                if auth:
                    headers, body = self._api_client.apply_auth_data(
                        conn, headers, body)
                log_body = None
                try:
                    content_type = self._headers.get('Content-Type', None)
                    if content_type == const.FGD_CONTENT_TYPE:
                        log_body = 'byte stream'
                    elif content_type == const.DEFAULT_CONTENT_TYPE:
                        body = jsonutils.dumps(self._body)
                        log_body = body
                    LOG.debug("Issuing request: self._method = [%(method)s], "
                              "url= %(url)s, body=%(body)s, "
                              "headers=%(headers)s",
                              {'method': self._method, "url": url,
                               "body": log_body, "headers": headers})
                    conn.request(self._method, url, body, headers)
                except Exception as e:
                    with excutils.save_and_reraise_exception():
                        LOG.warning(
                            _LW("[%(rid)d] Exception issuing request: %(e)s"),
                            {'rid': self._rid(), 'e': e})

                response = conn.getresponse()
                content_type = response.getheader('content-type') or ''
                response.content_type = content_type
                response.body = response.read()
                response.headers = response.getheaders()
                if DEFAULT_CONTENT_TYPE in content_type and response.body:
                    response_body = jsonutils.loads(response.body)
                elif content_type == const.FGD_CONTENT_TYPE:
                    response_body = 'byte stream'
                else:
                    response_body = response.body
                elapsed_time = time.time() - issued_time
                LOG.debug("@@@@@@ [ _issue_request ] [%(rid)d] "
                          "Completed request '%(conn)s': "
                          "%(status)s (%(elapsed)s seconds), "
                          "request.url: %(url)s, "
                          "request.method: %(method)s, "
                          "request.headers: %(headers)s, "
                          "request.body %(body)s,"
                          "response.headers: %(response.headers)s, "
                          "response.body: %(response.body)s",
                          {'rid': self._rid(),
                           'conn': self._request_str(conn, url),
                           'status': response.status,
                           'elapsed': elapsed_time,
                           'method': self._method, "url": url,
                           'headers': headers, 'body': log_body,
                           'response.headers': response.headers,
                           'response.body': response_body})
                if self._api_client.auth_required(response):
                    # if response.headers:
                    login_msg = self._api_client.login_msg()
                    if auth is None and login_msg:
                        # The connection still has no valid cookie despite
                        # attempts to authenticate and the request has failed
                        # with unauthorized status code. If this isn't a
                        # a request to authenticate, we should abort the
                        # request since there is no point in retrying.
                        if self._url != jsonutils.loads(login_msg)['path']:
                            self._abort = True

                    # If request is unauthorized, clear the session cookie
                    # for the current provider so that subsequent requests
                    # to the same provider triggers re-authentication.
                    self._api_client.set_auth_data(conn, None)

                elif 503 == response.status:
                    is_conn_service_unavail = True

                if response.status not in [301, 307]:
                    break
                elif redirects >= self._redirects:
                    LOG.info(_LI("[%d] Maximum redirects exceeded, aborting "
                                 "request"), self._rid())
                    break
                redirects += 1
                conn, url = self._redirect_params(conn, response.headers,
                                                  self._client_conn is None)
                if url is None:
                    response.status = 500
                    break
                LOG.info(_LI("[%(rid)d] Redirecting request to: %(conn)s"),
                         {'rid': self._rid(),
                          'conn': self._request_str(conn, url)})
                # yield here, just in case we are not out of the loop yet
                eventlet.greenthread.sleep(0)
            # If we receive any of these responses, then
            # our server did not process our request and may be in an
            # errored state. Raise an exception, which will cause the
            # the conn to be released with is_conn_error == True
            # which puts the conn on the back of the client's priority
            # queue.
            if 500 == response.status or 501 < response.status:
                LOG.warning(_LW("[%(rid)d] Request '%(method)s %(url)s' "
                                "received: %(status)s"),
                            {'rid': self._rid(), 'method': self._method,
                             'url': self._url, 'status': response.status,
                             'body': getattr(response, 'body', None)})
            return response

        except Exception as e:
            elapsed_time = time.time() - issued_time
            if isinstance(e, httpclient.BadStatusLine):
                msg = "Invalid server response"
                log_func = LOG.debug
            else:
                msg = str(e)
                log_func = LOG.warning
            log_func(("[{rid}] Failed request '{conn}': '{msg}' "
                      "({elapsed} seconds), error type '{err}'.").format(
                rid=self._rid(), conn=self._request_str(conn, url),
                msg=msg, elapsed=elapsed_time, err=type(e)))
            self._request_error = e
            is_conn_error = True
            if isinstance(e, const.CONNECTION_EXCEPTIONS):
                self._api_client.release_connection(conn, is_conn_error,
                                                    is_conn_service_unavail,
                                                    rid=self._rid())
                raise e
            ex.Exinfo(e)
            return e

        finally:
            # Make sure we release the original connection provided by the
            # acquire_connection() call above.
            if self._client_conn is None:
                self._api_client.release_connection(conn, is_conn_error,
                                                    is_conn_service_unavail,
                                                    rid=self._rid())

    def _handle_request(self):
        """First level request handling."""
        attempt = 0
        timeout = 0
        badstatus = 0
        response = None
        while response is None and attempt <= self._retries:
            eventlet.greenthread.sleep(timeout)
            attempt += 1
            req = None
            try:
                req = self._issue_request()
            except const.CONNECTION_EXCEPTIONS as e:
                if badstatus <= DEFAULT_RETRIES:
                    badstatus += 1
                    attempt -= 1
                    msg = ("# request {method} {url} {body} error {e}"
                           ).format(method=self._method, url=self._url,
                                    body=self._body, e=e)
                    LOG.debug(msg)
                    continue
            # automatically raises any exceptions returned.
            if isinstance(req, httpclient.HTTPResponse):
                timeout = 0
                if attempt <= self._retries and not self._abort:
                    # currently there is a bug in fortios, it return 401 and
                    # 400 when a cookie is invalid, the change is to tolerant
                    # the bug to handle return 400 situation.
                    # when fortios fix the bug, here should use
                    # 'req.status in (401, 403)' instead
                    # 303 for fortipam cookie expiration code
                    if self._api_client.auth_required(req):
                        continue
                    elif req.status == 503:
                        timeout = 0.5
                        continue
                    # else fall through to return the error code

                LOG.debug("[%(rid)d] Completed request '%(method)s %(url)s'"
                          ": %(status)s",
                          {'rid': self._rid(), 'method': self._method,
                           'url': self._url, 'status': req.status})
                self._request_error = None
                response = req
            else:
                LOG.info(_LI('[%(rid)d] Error while handling request: '
                             '%(req)s'),
                         {'rid': self._rid(), 'req': req})
                self._request_error = req
                response = None
        return response

    def _redirect_params(self, conn, headers, allow_release_conn=False):
        """Process redirect response, create new connection if necessary.

        Args:
            conn: connection that returned the redirect response
            headers: response headers of the redirect response
            allow_release_conn: if redirecting to a different server,
                release existing connection back to connection pool.

        Returns: Return tuple(conn, url) where conn is a connection object
            to the redirect target and url is the path of the API request
        """
        url = None
        for name, value in headers:
            if name.lower() == "location":
                url = value
                break
        if not url:
            LOG.warning(_LW("[%d] Received redirect status without location "
                            "header field"), self._rid())
            return conn, None
        # Accept location with the following format:
        # 1. /path, redirect to same node
        # 2. scheme://hostname:[port]/path where scheme is https or http
        # Reject others
        # 3. e.g. relative paths, unsupported scheme, unspecified host
        result = urlparse.urlparse(url)
        if not result.scheme and not result.hostname and result.path:
            if result.path[0] == "/":
                if result.query:
                    url = "%s?%s" % (result.path, result.query)
                else:
                    url = result.path
                return conn, url  # case 1
            else:
                LOG.warning(_LW("[%(rid)d] Received invalid redirect location:"
                                "'%(url)s'"), {'rid': self._rid(), 'url': url})
                return conn, None  # case 3
        elif result.scheme not in ["http", "https"] or not result.hostname:
            LOG.warning(_LW("[%(rid)d] Received malformed redirect "
                            "location: %(url)s"),
                        {'rid': self._rid(), 'url': url})
            return conn, None  # case 3
        # case 2, redirect location includes a scheme
        # so setup a new connection and authenticate
        if allow_release_conn:
            self._api_client.release_connection(conn)
        conn_params = (result.hostname, result.port, result.scheme == "https")
        conn = self._api_client.acquire_redirect_connection(conn_params, True,
                                                            self._headers)
        if result.query:
            url = "%s?%s" % (result.path, result.query)
        else:
            url = result.path
        return conn, url

    def _rid(self):
        """Return current request id."""
        return self._request_id

    @property
    def request_error(self):
        """Return any errors associated with this instance."""
        return self._request_error

    def _request_str(self, conn, url):
        """Return string representation of connection."""
        return "%s %s%s" % (self._method, utils.ctrl_conn_to_str(conn),
                            url)
