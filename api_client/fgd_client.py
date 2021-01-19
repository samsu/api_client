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

from Crypto.Cipher import DES
from datetime import datetime
from oslo_log import log as logging
import struct
import zlib

from . import base
from . import constants as const
from . import client

from .common import utils
from .templates import fgd as default_template

LOG = logging.getLogger(__name__)

DEFAULT_HTTP_TIMEOUT = const.DEFAULT_HTTP_TIMEOUT
DEFAULT_RETRIES = const.DEFAULT_RETRIES
DEFAULT_REDIRECTS = const.DEFAULT_REDIRECTS


class FortiGuardApiClient(client.ApiClient):
    """The FortiOS API Client."""

    user_agent = 'FortiGuard Python API Client'

    def __init__(self, api_providers, template=None, user=None, password=None,
                 key_file=None, cert_file=None, ca_file=None, ssl_sni=None,
                 concurrent_connections=base.DEFAULT_CONCURRENT_CONNECTIONS,
                 gen_timeout=base.GENERATION_ID_TIMEOUT,
                 use_https=True,
                 connect_timeout=base.DEFAULT_CONNECT_TIMEOUT,
                 http_timeout=DEFAULT_HTTP_TIMEOUT,
                 retries=DEFAULT_RETRIES,
                 redirects=DEFAULT_REDIRECTS,
                 auto_login=True, singlethread=False, **kwargs):
        """Constructor. Adds the following:
        :param api_providers: a list of tuples of the form: (host, port,
            is_ssl)
        :param http_timeout: how long to wait before aborting an
            unresponsive controller (and allow for retries to another
            controller in the cluster)
        :param retries: the number of http/https request to retry.
        :param redirects: the number of concurrent connections.
        """
        super(FortiGuardApiClient, self).__init__(
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
        self.message = {}
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
        self.resp_type = None
        self._fgd_params = {}
        for key in const.FGD_OPTIONS:
            self._fgd_params[key] = kwargs.get(key, None)

    def request(self, opt, content_type=const.FGD_CONTENT_TYPE, **message):
        resp = super(FortiGuardApiClient,
                     self).request(opt, content_type, **message)
        return resp

    def _createPackage(self, obj_list, fw_version):
        package_format = const.PHEADER_FORMAT
        pheader = struct.Struct(package_format)
        pheader_size = struct.calcsize(package_format)
        now = datetime.utcnow()
        date_time = now.strftime("%Y%m%d%H%M")
        total_size = 0
        for obj in obj_list:
            total_size += len(obj)
        header_args = [0x46545550, fw_version.encode('utf8'), len(obj_list), total_size,
                       pheader_size, date_time.encode('utf8'), '\0'.encode('utf8') * 24,
                       self._fgd_params['pheader_crc_key']]
        pheader = pheader.pack(*tuple(header_args))
        header_chksum = zlib.crc32(pheader) & 0xffffffff
        header_args[-1] = header_chksum
        pheader = struct.pack(package_format, *tuple(header_args))
        package = pheader
        for obj in obj_list:
            package = package + obj
        return package

    def _createObject(self, obj, obj_type, subtype, desc, version, fw_version,
                     flags):
        obj_size = len(obj)
        data_crc = zlib.crc32(obj) & 0xffffffff
        header_format = const.OHEADER_FORMAT
        header_size = struct.calcsize(header_format)
        header_args = list(
            [obj_type.encode('utf8'), desc.encode('utf8'), version.encode('utf8'),
             flags, obj_size, header_size, fw_version.encode('utf8'),
             '\0'.encode('utf8') * 44, 0, 0, subtype, data_crc,
             self._fgd_params['oheader_crc_key']])
        header = struct.pack(header_format, *tuple(header_args))
        header_checksum = zlib.crc32(header) & 0xffffffff
        header_args[-1] = header_checksum
        header = struct.pack(header_format, *tuple(header_args))
        packed_obj = struct.pack(str(header_size) + 's' + str(obj_size) + 's',
                                 header, obj)
        return packed_obj

    def _pack_req(self, body, fw_version):
        body = body + '\r\n\r\n'
        obj = self._createObject(body.encode('utf8'), 'FCPC', 0, 'Command Object', '0',
                                 fw_version, const.FGD_REQ_FLAGS)
        return self._createPackage([obj], fw_version)

    def _unpack_resp(self, package, resp_type):
        pheader_size = struct.calcsize(const.PHEADER_FORMAT)
        pheader = package[:pheader_size]
        pheader = struct.unpack_from(const.PHEADER_FORMAT, pheader)
        obj_list = package[pheader_size:]
        oheader_size = struct.calcsize(const.OHEADER_FORMAT)
        obj_pointer = 0
        for i in range(0, pheader[2]):
            obj_header = obj_list[obj_pointer:obj_pointer + oheader_size]
            obj_header = struct.unpack_from(const.OHEADER_FORMAT, obj_header)
            if resp_type.encode('utf8') != obj_header[0]:
                if obj_header[0] == 'FCPR'.encode('utf8'):
                    resp = obj_list[obj_pointer + oheader_size:obj_pointer +
                                    oheader_size + obj_header[4]]
                    if obj_header[3] & self._fgd_params['encrypt_des_flag']:
                        resp = self.decrypt(resp,
                                            self._fgd_params['des_key_str'])
                    resp_items = resp.split('|')
                    response_code_items = resp_items[-1].split(':')
                    if len(response_code_items) < 2:
                        continue
                    response_code = response_code_items[1]
                    if response_code != '200':
                        return None
                obj_pointer += oheader_size + obj_header[4]
                continue
            obj = obj_list[obj_pointer + obj_header[5]:obj_pointer +
                           oheader_size + obj_header[4]]
            if obj_header[3] & self._fgd_params['encrypt_des_flag']:
                obj = self.decrypt(obj, self._fgd_params['des_key_str'])
            if obj_header[3] & self._fgd_params['compress_gzip_flag']:
                obj = zlib.decompress(obj)
            return obj
        return None

    def render(self, opt, content_type=const.FGD_CONTENT_TYPE, **message):
        if 'fw_version' not in message:
            message['fw_version'] = const.FTC_FW_VERSION
        msg = super(FortiGuardApiClient,
                    self).render(opt, content_type, **message)
        body = bytearray(self._pack_req(msg['body'],
                                        message.get('fw_version')))
        msg['body'] = body
        return msg

    def request_response_body(self, response, **kwargs):
        return self._unpack_resp(response.body, kwargs['resp_type'])

    @staticmethod
    def decrypt(string, key):
        cipher = DES.new(key, DES.MODE_CBC, key)
        decrypted_string = ''
        for i in range(0, len(string), len(key)):
            decrypted_string += cipher.decrypt(string[i:i + len(key)]).decode('utf8')
        return decrypted_string.split('\r\n\r\n')[0]

