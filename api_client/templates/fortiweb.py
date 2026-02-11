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

GET_SERVERPOOL_SERVER = """
{
    {% if name is defined %}
        "path": "/api/v2.0/cmdb/server-policy/server-pool/pserver-list?mkey={{ name }}",
    {% else %}
        "path": "/api/v2.0/cmdb/server-policy/server-pool/pserver-list",
    {% endif %}
    "method": "GET"
}
"""

ADD_SERVERPOOL_SERVER = """
{
    "path": "/api/v2.0/cmdb/server-policy/server-pool/pserver-list?mkey={{ name }}",
    "body": {
        {%
            set _options = {
                "server-type": server_type,
                "ip": ip,
                "port": port,
                "domain": domain,
                "status": status,
                "backup-server": backup_server,
                "conn-limit": conn_limit,
                "weight": weight,
                "ssl": ssl,
                "ssl-cipher": ssl_cipher,
                "hsts-header": hsts_header,
                "hsts-max-age": hsts_max_age,
                "health-check-inherit": health_check_inherit,
                "tls13-custom-cipher": tls13_custom_cipher,
                "ssl-custom-cipher": ssl_custom_cipher,
                "client-certificate-forwarding": client_certificate_forwarding,
                "client-certificate-forwarding-sub-header": client_certificate_forwarding_sub_header,
                "client-certificate-forwarding-cert-header": client_certificate_forwarding_cert_header
            }
        %}
        "data": {
        {% for k, v in _options.items() if v is defined %}
            "{{ k }}": "{{ v }}"
            {{ "," if not loop.last }}
        {% endfor %}
        }
    },
    "method": "POST"
}
"""

DELETE_SERVERPOOL_SERVER = """
{
    "path": "/api/v2.0/cmdb/server-policy/server-pool/pserver-list?mkey={{ name }}&sub_mkey={{ server_id }}",
    "method": "DELETE"
}
"""

MODIFY_SERVER_POOL_SERVER = """
{
    "path": "/api/v2.0/cmdb/server-policy/server-pool/pserver-list?mkey={{ name }}&sub_mkey={{ server_id }}",
    "body": {
        {%
            set _options = {
                "server-type": server_type,
                "ip": ip,
                "port": port,
                "domain": domain,
                "status": status,
                "backup-server": backup_server,
                "conn-limit": conn_limit,
                "weight": weight,
                "ssl": ssl,
                "ssl-cipher": ssl_cipher,
                "hsts-header": hsts_header,
                "hsts-max-age": hsts_max_age,
                "health-check-inherit": health_check_inherit,
                "tls13-custom-cipher": tls13_custom_cipher,
                "ssl-custom-cipher": ssl_custom_cipher,
                "client-certificate-forwarding": client_certificate_forwarding,
                "client-certificate-forwarding-sub-header": client_certificate_forwarding_sub_header,
                "client-certificate-forwarding-cert-header": client_certificate_forwarding_cert_header
            }
        %}
        "data": {
        {% for k, v in _options.items() if v is defined %}
            "{{ k }}": "{{ v }}"
            {{ "," if not loop.last }}
        {% endfor %}
        }
    },
    "method": "PUT"
}
"""
