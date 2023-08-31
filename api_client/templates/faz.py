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
#    FortiAnalyzer API request format templates.

# About api request message naming regulations:
# Prefix         HTTP method
# ADD_XXX      -->    POST
# SET_XXX      -->    PUT
# DELETE_XXX   -->    DELETE
# GET_XXX      -->    GET
# MODIFY_XXX   -->    PATCH


# login to get session
LOGIN = """
{
    "path": "/jsonrpc",
    "method": "POST",
    "body": {
        "method": "exec",
        "params": [
            {
                "url": "/sys/login/user",
                "data": {
                    "user": "{{ user }}",
                    "passwd": "{{ password }}"
                }
            }
        ],
        {% set _id = uuid() %}
        "id": "{{ _id }}"
    }
}
"""

ADD_DEVICE = """
{
    "path": "/jsonrpc",
    "method": "POST",
    "body": {
        "method": "exec",
        "params": [
            {
                "data": {
                    "adom": "{{ adom }}",
                    "device": {
                        "sn": "{{ sn }}",
                        "mgmt_mode": "faz"
                    }
                },
                "url": "/dvm/cmd/add/device"
            }
        ],
        "session": "{{ session }}",
        {% set _id = uuid() %}
        "id": "{{ _id }}"
    }
}
"""

DELETE_DEVICE = """
{
    "path": "/jsonrpc",
    "method": "POST",
    "body": {
        "method": "exec",
        "params": [
            {
                "data": {
                    "adom": "{{ adom }}",
                    "device": "{{ sn }}"
                },
                "url": "/dvm/cmd/del/device"
            }
        ],
        "session": "{{ session }}",
        {% set _id = uuid() %}
        "id": "{{ _id }}"
    }
}
"""

GET_SYNTAX = """
{
    "path": "/jsonrpc",
    "method": "POST",
    "body": {
        "method": "get",
        "params": [
            {
                "url": "/cli/global/system/log-forward",
                "option": "syntax"
            }
        ],
        "session": "{{ session }}",
        {% set _id = uuid() %}
        "id": "{{ _id }}"

    }
}
"""

GET_FORWARDERS = """
{
    "path": "/jsonrpc",
    "method": "POST",
    "body": {
        "method": "get",
        "params": [
            {
                "url": "/cli/global/system/log-forward"
            }
        ],
        "session": "{{ session }}",
        {% set _id = uuid() %}
        "id": "{{ _id }}"
    }
}
"""

GET_FORWARDER = """
{
    "path": "/jsonrpc",
    "method": "POST",
    "body": {
        "method": "get",
        "params": [
            {
                {% if fields is defined and fields %}
                    "fields": ["id", "server-name"],
                {% endif %}
                {% if name is defined %}
                    "filter": [
                        "server-name", "==", "{{ name }}"
                    ],
                {% endif %}
                {% if loadsub is defined %}
                    "loadsub": "{{ loadsub }}",
                {% else %}
                    "loadsub": 1,
                {% endif %}
                {% if id is defined %}
                    "url": "/cli/global/system/log-forward/{{ id }}"
                {% else %}
                    "url": "/cli/global/system/log-forward"
                {% endif %}
            }
        ],
        "session": "{{ session }}",
        {% set _id = uuid() %}
        "id": "{{ _id }}"
    }
}
"""

ADD_FORWARDER = """
{
    "path": "/jsonrpc",
    "method": "POST",
    "body": {
        "method": "add",
        "params": [
            {
                "data": [
                    {
                        {% set _options = {
                            "server-addr": address,
                            "server-name": name,
                            "fwd-max-delay": delay,
                            "fwd-reliable": reliable,
                            "peer-cert-cn": peercn
                        } %}
                        {% for k, v in _options.items() if v is defined %}
                            "{{ k }}": "{{ v }}",
                        {% endfor %}
                        "id": -1,
                        "device-filter": [
                            {
                                "action": "include",
                                "adom": "{{ adom }}",
                                "device": "{{ sn }}",
                                "id": -1
                            }
                        ],
                        "fwd-server-type": "fortianalyzer",
                        "mode": "forwarding"
                    }
                ],
                "url": "/cli/global/system/log-forward"
            }
        ],
        "session": "{{ session }}",
        {% set _id = uuid() %}
        "id": "{{ _id }}"
    }
}
"""

MODIFY_FORWARDER = """
{
    "path": "/jsonrpc",
    "method": "POST",
    "body": {
        "method": "update",
        "params": [
            {
                "data": {
                    {% set _options = {
                        "server-addr": address,
                        "server-name": name,
                        "fwd-max-delay": delay,
                        "fwd-reliable": reliable,
                        "peer-cert-cn": peercn
                    } %}
                    {% for k, v in _options.items() if v is defined %}
                        "{{ k }}": "{{ v }}",
                    {% endfor %}
                    "id": {{id}},
                    {% if filter_id is defined %}
                        "device-filter": [
                            {
                                {% if adom is defined %}
                                    "adom": "{{ adom }}",
                                {% endif %}
                                {% if sn is defined %}
                                    "device": "{{ sn }}",
                                {% endif %}
                                "id": "{{ filter_id }}",
                                "action": "include"
                            }
                        ],
                    {% endif %}
                    "fwd-server-type": "fortianalyzer",
                    "mode": "forwarding"
                },
                "url": "/cli/global/system/log-forward"
            }
        ],
        "session": "{{ session }}",
        {% set _id = uuid() %}
        "id": "{{ _id }}"
    }
}
"""

DELETE_FORWARDER = """
{
    "path": "/jsonrpc",
    "method": "POST",
    "body": {
        "method": "delete",
        "params": [
            {
                "url": "/cli/global/system/log-forward/{{ id }}"
            }
        ],
        "session": "{{ session }}",
        {% set _id = uuid() %}
        "id": "{{ _id }}"
    }
}
"""
