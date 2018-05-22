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
#

try:
    import httplib
except ImportError:
    import http.client as httplib

try:
    from imp import load_source as import_module_file
except ImportError:
    from importlib.util import spec_from_file_location as import_module_file

from os import listdir
from os.path import dirname
from oslo_utils import importutils

from api_client import constants as consts


def ctrl_conn_to_str(conn):
    """Returns a string representing a connection URL to the controller."""
    if isinstance(conn, httplib.HTTPSConnection):
        proto = "https://"
    elif isinstance(conn, httplib.HTTPConnection):
        proto = "http://"
    else:
        raise TypeError('Invalid connection type: %s' % type(conn))
    return "%s%s:%s" % (proto, conn.host, conn.port)


def import_file_module(file_path, file_name, module_name=None):
    if not file_name.endswith('.py'):
        file_name = '.'.join([file_name, 'py'])
    module_name = module_name or file_name[:-3]
    return import_module_file(module_name, '/'.join([file_path, file_name]))


def get_api_service_module(file_path):
    """
    :param file_path: file is the file path
    e.g.
        '/usr/lib/python2.7/site-packages/test/api/v1/hello.pyc'
    :param file_name: api service filename, e.g. 'hello'
    :return:
    """
    for postfix in ['.py', '.pyc']:
        if file_path.endswith(postfix):
            file_path = file_path.replace(postfix, '')
    file_path = file_path.split('/')
    _module = file_path[-4:]
    _module.insert(1, 'services')
    _module = '.'.join(_module)
    return importutils.import_module(_module)


def get_module_files(int_path):
    path = dirname(__file__).split('/')[:-1]
    path = '/'.join(path)
    path = ''.join([path, int_path])
    files = [f for f in listdir(path) if
             f.endswith('.py') and f != '__init__.py']
    return path, files


def translate_uri_chars(var):
    for old, new in consts.URI_CHAR_CODES.iteritems():
        var = var.replace(old, new)
    return var
