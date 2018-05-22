# Copyright 2015 Fortinet, Inc.
# All rights reserved.
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

GENERATION_ID_TIMEOUT = -1
DEFAULT_CONCURRENT_CONNECTIONS = 1
DEFAULT_CONNECT_TIMEOUT = 35
CONN_IDLE_TIMEOUT = 60 * 15

DEFAULT_HTTP_TIMEOUT = 300
DEFAULT_RETRIES = 0
DEFAULT_REDIRECTS = 1
DEFAULT_API_REQUEST_POOL_SIZE = 1
DEFAULT_MAXIMUM_REQUEST_ID = 4294967295
DOWNLOAD_TIMEOUT = 180

DEFAULT_HTTP_HEADERS = {
    'User-Agent': 'Fortinet Python API Client',
    'Content-Type': 'application/json'
}

URI_CHAR_CODES = {
    '<': '%3C',
    '>': '%3E',
    '#': '%23',
    '%': '%25',
    '{': '%7B',
    '}': '%7D',
    '|': '%7C',
    '\\': '%5C',
    '^': '%5E',
    '~': '%7E',
    '[': '%5B',
    ']': '%5D',
    '`': '%60',
    ';': '%3B',
    '/': '%2F',
    '?': '%3F',
    ':': '%3A',
    '@': '%40',
    '=': '%3D',
    '&': '%26',
    '$': '%24',
    '+': '%2B',
    '"': '%22',
    ' ': '%20'
}
