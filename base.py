# Copyright 2015 Fortinet, Inc.
#
# All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import abc
import base64

try:
    import Cookie
    import httplib
except ImportError:
    import http.client as httplib
    from http import cookies as Cookie
import time

from oslo_log import log as logging
import six
import socket
import ssl

from _i18n import _LE, _LI, _LW
import common.utils as utils
import constants as const


LOG = logging.getLogger(__name__)
GENERATION_ID_TIMEOUT = const.GENERATION_ID_TIMEOUT
DEFAULT_CONCURRENT_CONNECTIONS = const.DEFAULT_CONCURRENT_CONNECTIONS
DEFAULT_CONNECT_TIMEOUT = const.DEFAULT_CONNECT_TIMEOUT


@six.add_metaclass(abc.ABCMeta)
class ApiClientBase(object):
    """An abstract baseclass for all API client implementations."""

    CONN_IDLE_TIMEOUT = const.CONN_IDLE_TIMEOUT

    def _create_connection(self, host, port, is_ssl):
        if is_ssl:
            try:
                context = ssl._create_unverified_context(
                    cert_reqs=ssl.CERT_NONE)
                return httplib.HTTPSConnection(host, port,
                                               timeout=self._connect_timeout,
                                               context=context)
            except (ImportError, AttributeError):
                return httplib.HTTPSConnection(host, port,
                                               timeout=self._connect_timeout)

        return httplib.HTTPConnection(host, port,
                                      timeout=self._connect_timeout)

    @staticmethod
    def _conn_params(http_conn):
        is_ssl = isinstance(http_conn, httplib.HTTPSConnection)
        return (http_conn.host, http_conn.port, is_ssl)

    @property
    def user(self):
        return self._user

    @property
    def password(self):
        return self._password

    @property
    def config_gen(self):
        # If NSX_gen_timeout is not -1 then:
        # Maintain a timestamp along with the generation ID.  Hold onto the
        # ID long enough to be useful and block on sequential requests but
        # not long enough to persist when Onix db is cleared, which resets
        # the generation ID, causing the DAL to block indefinitely with some
        # number that's higher than the cluster's value.
        if self._gen_timeout != -1:
            ts = self._config_gen_ts
            if ts is not None:
                if (time.time() - ts) > self._gen_timeout:
                    return None
        return self._config_gen

    @config_gen.setter
    def config_gen(self, value):
        if self._config_gen != value:
            if self._gen_timeout != -1:
                self._config_gen_ts = time.time()
        self._config_gen = value

    def auth_data(self, conn):
        # auth_data could be cookie or other fields with authentication
        # info in http headers.
        auth_data = None
        data = self._get_provider_data(conn)
        if data:
            auth_data = data[1]
        return auth_data

    def format_auth_basic(self):
        auth = '{}:{}'.format(self._user, self._password)
        return "Basic {}".format(base64.encodestring(auth).replace('\n', ''))

    def set_auth_basic(self, conn, auth_basic=None):
        data = self._get_provider_data(conn)
        if data:
            self._set_provider_data(conn, (data[0], auth_basic))

    def set_auth_data(self, conn, *data):
        if self._auth_sch in const.AUTH_FUNC_MAPS:
            auth_func = getattr(self, const.AUTH_FUNC_MAPS[self._auth_sch])
            return auth_func(conn, *data)
        else:
            LOG.error(_LE("Invalid authentication scheme: %(sch)s"),
                      {'sch': self._auth_sch})
            raise ValueError

    @staticmethod
    def format_cookie(cookie):
        if not cookie:
            return None
        try:
            fmt_headers = {}
            cookies = Cookie.SimpleCookie(cookie)
            for key, morsel in six.iteritems(cookies):
                if "ccsrftoken" in morsel.key:
                    morsel.coded_value = morsel.value
                    fmt_headers["X-CSRFTOKEN"] = morsel.value
                    break
            fmt_headers["Cookie"] = cookies.output(header="").lstrip()
            return fmt_headers
        except (Cookie.CookieError, KeyError):
            LOG.error(_LE("The cookie ccsrftoken cannot be formatted"))
            raise Cookie.CookieError

    def set_auth_cookie(self, conn, cookie=None):
        data = self._get_provider_data(conn)
        if data:
            cookie = self.format_cookie(cookie)
            self._set_provider_data(conn, (data[0], cookie))

    def acquire_connection(self, auto_login=True, headers=None, rid=-1):
        '''Check out an available HTTPConnection instance.

        Blocks until a connection is available.
        :auto_login: automatically logins before returning conn
        :headers: header to pass on to login attempt
        :param rid: request id passed in from request eventlet.
        :returns: An available HTTPConnection instance or None if no
                 api_providers are configured.
        '''
        if self._conn_pool.empty():
            LOG.debug("[%d] Waiting to acquire API client connection.", rid)
        priority, conn = self._conn_pool.get()
        now = time.time()
        if getattr(conn, 'last_used', now) < now - self.CONN_IDLE_TIMEOUT:
            LOG.info(_LI("[%(rid)d] Connection %(conn)s idle for "
                         "%(sec)0.2f seconds; reconnecting."),
                     {'rid': rid,
                      'conn': utils.ctrl_conn_to_str(conn),
                      'sec': now - conn.last_used})
            conn = self._create_connection(*self._conn_params(conn))
            self.set_auth_data(conn)
        conn.last_used = now
        conn.priority = priority  # stash current priority for release
        qsize = self._conn_pool.qsize()
        LOG.debug("[%(rid)d] Acquired connection %(conn)s. %(qsize)d "
                  "connection(s) available.",
                  {'rid': rid, 'conn': utils.ctrl_conn_to_str(conn),
                   'qsize': qsize})
        if auto_login and self.auth_data(conn) is None:
            self._wait_for_login(conn, headers)
        return conn

    def release_connection(self, http_conn, bad_state=False,
                           service_unavail=False, rid=-1):
        '''Mark HTTPConnection instance as available for check-out.

        :param http_conn: An HTTPConnection instance obtained from this
            instance.
        :param bad_state: True if http_conn is known to be in a bad state
                (e.g. connection fault.)
        :service_unavail: True if http_conn returned 503 response.
        :param rid: request id passed in from request eventlet.
        '''
        conn_params = self._conn_params(http_conn)
        if self._conn_params(http_conn) not in self._api_providers:
            LOG.debug("[%(rid)d] Released connection %(conn)s is not an "
                      "API provider for the cluster",
                      {'rid': rid,
                       'conn': utils.ctrl_conn_to_str(http_conn)})
            return
        elif hasattr(http_conn, "no_release"):
            return

        if bad_state:
            # Reconnect to provider.
            LOG.warning(_LW("[%(rid)d] Connection returned in bad state, "
                            "reconnecting to %(conn)s"),
                        {'rid': rid,
                         'conn': utils.ctrl_conn_to_str(http_conn)})
            http_conn.close()
            http_conn = self._create_connection(*self._conn_params(http_conn))
            conns = []
            while not self._conn_pool.empty():
                priority, conn = self._conn_pool.get()
                if self._conn_params(conn) == conn_params:
                    conn.close()
                    continue
                conns.append((priority, conn))
            for priority, conn in conns:
                self._conn_pool.put((priority, conn))
            priority = self._next_conn_priority
            self._next_conn_priority += 1

        elif service_unavail:
            # http_conn returned a service unaviable response, put other
            # connections to the same controller at end of priority queue,
            conns = []
            while not self._conn_pool.empty():
                priority, conn = self._conn_pool.get()
                if self._conn_params(conn) == conn_params:
                    priority = self._next_conn_priority
                    self._next_conn_priority += 1
                conns.append((priority, conn))
            for priority, conn in conns:
                self._conn_pool.put((priority, conn))
            priority = self._next_conn_priority
            self._next_conn_priority += 1
        else:
            priority = http_conn.priority

        self._conn_pool.put((priority, http_conn))
        LOG.debug("[%(rid)d] Released connection %(conn)s. %(qsize)d "
                  "connection(s) available.",
                  {'rid': rid, 'conn': utils.ctrl_conn_to_str(http_conn),
                   'qsize': self._conn_pool.qsize()})

    def _wait_for_login(self, conn, headers=None):
        '''Block until a login has occurred for the current API provider.'''
        data = self._get_provider_data(conn)
        if data is None:
            LOG.error(_LE("Login request for an invalid connection: '%s'"),
                      utils.ctrl_conn_to_str(conn))
            return
        provider_sem = data[0]
        if provider_sem.acquire(blocking=False):
            try:
                cookie = self._login(conn, headers)
                self.set_auth_data(conn, cookie)
            finally:
                provider_sem.release()
        else:
            LOG.debug("Waiting for auth to complete")
            # Wait until we can acquire then release
            provider_sem.acquire(blocking=True)
            provider_sem.release()

    def _get_provider_data(self, conn_or_conn_params, default=None):
        """Get data for specified API provider.

        Args:
            conn_or_conn_params: either a HTTP(S)Connection object or the
                resolved conn_params tuple returned by self._conn_params().
            default: conn_params if ones passed aren't known
        Returns: Data associated with specified provider
        """
        conn_params = self._normalize_conn_params(conn_or_conn_params)
        return self._api_provider_data.get(conn_params, default)

    def _set_provider_data(self, conn_or_conn_params, data):
        """Set data for specified API provider.

        Args:
            conn_or_conn_params: either a HTTP(S)Connection object or the
                resolved conn_params tuple returned by self._conn_params().
            data: data to associate with API provider
        """
        conn_params = self._normalize_conn_params(conn_or_conn_params)
        if data is None:
            del self._api_provider_data[conn_params]
        else:
            self._api_provider_data[conn_params] = data

    def _normalize_conn_params(self, conn_or_conn_params):
        """Normalize conn_param tuple.

        Args:
            conn_or_conn_params: either a HTTP(S)Connection object or the
                resolved conn_params tuple returned by self._conn_params().

        Returns: Normalized conn_param tuple
        """
        if (not isinstance(conn_or_conn_params, tuple) and
            not isinstance(conn_or_conn_params, httplib.HTTPConnection)):
            LOG.debug("Invalid conn_params value: '%s'",
                      str(conn_or_conn_params))
            return conn_or_conn_params
        if isinstance(conn_or_conn_params, httplib.HTTPConnection):
            conn_params = self._conn_params(conn_or_conn_params)
        else:
            conn_params = conn_or_conn_params
        host, port, is_ssl = conn_params
        if port is None:
            port = 443 if is_ssl else 80
        return (host, port, is_ssl)


class HTTPSClientAuthConnection(httplib.HTTPSConnection):
    """
    Class to make a HTTPS connection, with support for
    full client-based SSL Authentication

    :see http://code.activestate.com/recipes/
            577548-https-httplib-client-connection-with-certificate-v/
    """

    def __init__(self, host, port, key_file, cert_file, ca_file,
                 ssl_sni=None, timeout=None):
        httplib.HTTPSConnection.__init__(self, host, port,
                                         key_file=key_file,
                                         cert_file=cert_file)
        self.key_file = key_file
        self.cert_file = cert_file
        self.ca_file = ca_file
        self.timeout = timeout
        # SSL server_name_indication
        self.ssl_sni = ssl_sni

    def connect(self):
        """
        Connect to a host on a given (SSL) port.
        If ca_file is pointing somewhere, use it to check Server Certificate.

        Redefined/copied and extended from httplib.py:1105 (Python 2.6.x).
        This is needed to pass cert_reqs=ssl.CERT_REQUIRED as parameter to
        ssl.wrap_socket(), which forces SSL to check server certificate against
        our client certificate.
        """
        sock = socket.create_connection((self.host, self.port), self.timeout)
        if self._tunnel_host:
            self.sock = sock
            self._tunnel()
        # If there's no CA File, don't force Server Certificate Check
        if self.ca_file:
            self.sock = wrap_socket(sock, self.key_file, self.cert_file,
                                    ca_certs=self.ca_file,
                                    cert_reqs=ssl.CERT_REQUIRED,
                                    server_hostname=self.ssl_sni)
        else:
            self.sock = wrap_socket(sock, self.key_file, self.cert_file,
                                        cert_reqs=ssl.CERT_NONE)


def wrap_socket(sock, keyfile=None, certfile=None,
                server_side=False, cert_reqs=ssl.CERT_NONE,
                ssl_version=ssl.PROTOCOL_SSLv23, ca_certs=None,
                do_handshake_on_connect=True,
                suppress_ragged_eofs=True,
                ciphers=None, server_hostname=None):
    return ssl.SSLSocket(sock=sock, keyfile=keyfile, certfile=certfile,
                         server_side=server_side, cert_reqs=cert_reqs,
                         ssl_version=ssl_version, ca_certs=ca_certs,
                         do_handshake_on_connect=do_handshake_on_connect,
                         suppress_ragged_eofs=suppress_ragged_eofs,
                         ciphers=ciphers, server_hostname=server_hostname)


if __name__ == '__main__':
    # Little test-case of our class
    from oslo_serialization import jsonutils

    host = "172.30.38.89"
    port = "443"
    url = "/FortiGlobal/FortiCASB.asmx/Process"
    method = "POST"
    message = {
        'd': {
            '__type': 'FortiGlobal.FortiCASBAccountInfoRequest',
            '__version': '1',
            '__SW_version': 'xxxx',
            '__SW_build': 'yyyyy',
            'User_ID': '395939'
        }
    }

    key_file = "/root/subca/cert201706291056.key"
    cert_file = "/root/subca/cert201706291056.crt"
    cert_reqs = "/root/subca/cert201706291056.csr"
    ca_file = "/root/subca/chain.pem"
    server_hostname = "fortinet-ca2.fortinet.com"

    headers = {"Content-type": "application/json", "Host": server_hostname}

    conn = HTTPSClientAuthConnection(host, port, key_file=key_file,
                                     cert_file=cert_file, ca_file=ca_file,
                                     ssl_sni=server_hostname)
    body = jsonutils.dumps(message)
    conn.request(method, url, body, headers)

    response = conn.getresponse()
    response.body = response.read()
    response.headers = response.getheaders()
    statuscode = response.status
    res = response.body
    header = response.headers
    print "The testing starting:"
    print "API server: ", host
    print "server port: 443"
    print "Request.url: ", url
    print "Request.method: ", method
    print "Request.headers: ", headers
    print "Request.body: ", body
    print "Response.status: ", statuscode
    print "Response.headers: ", header
    print "Response.body: ", res
    print "Response.reason: ", response.reason
    print "### The End ###"
    conn.close()
