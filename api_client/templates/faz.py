# Copyright (c) 2017 Fortinet, Inc.
# All Rights Reserved.
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

#    FortiAuthenticator API request format templates.

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
    "id": 1
}
"""

ADD_DEVICE = """
{
  "method": "exec",
  "params": [
    {
      "data": {
        "adom": "{{ adom }}",
        "device": {
          "sn": "{{ sn }}",
          "mgmt_mode":"faz"
        }
      },
      "url": "/dvm/cmd/add/device"
    }
  ],
  "session": "{{ session }}",
  "id": 1
}
"""

DEL_DEVICE = """
{
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
  "id": 1
}
"""

GET_SYNTAX = """
{
    "method": "get",
    "params": [{
        "url": "/cli/global/system/log-forward",
        "option": "syntax"
    }],
    "id": "1",
    "session": "{{ session }}"
}
"""

GET_FORWARDERS = """
{
    "method": "get",
    "params": [{
        "url": "/cli/global/system/log-forward"
    }],
    "id": 1,
    "session": "{{ session }}"
}
"""

GET_FORWARDER = """
{
    "method": "get",
    "params": [{
        "url": "/cli/global/system/log-forward/{{ id }}"
    }],
    "id": 1,
    "session": "{{ session }}"
}
"""

ADD_FORWARDER = """
{
  "method": "add",
  "params": [
    {
      "data": [
        {
          "server-addr": "{{ address }}",
          "server-name": "{{ name }}",
          "id": {{ id }},
          "device-filter": [
            {
              "action": "include",
              "adom": "{{ adom }}",
              "device": "{{ sn }}",
              "id": 1
            }
          ],
          "mode": "forwarding",
          "fwd-max-delay": "{{ delay }}",
          "fwd-server-type": "fortianalyzer",
          "fwd-reliable": "{{ reliable }}",
          {% if peercn is defined %}
            "peer-cert-cn": "{{ peercn }}",
          {% endif %}
          "fwd-secure": "{{ secure }}"
        }
      ],
      "url": "/cli/global/system/log-forward"
    }
  ],
  "id": 1,
  "session": "{{ session }}"
}
"""

EDIT_FORWARDER = """
{
  "method": "update",
  "params": [
    {
      "data": {
        "server-addr": "{{ address }}",
          "server-name": "{{ name }}",
          "id": {{ id }},
          "device-filter": [
            {
              "action": "include",
              "adom": "{{ adom }}",
              "device": "{{ sn }}",
              "id": 1
            }
          ],
          "mode": "forwarding",
          "fwd-max-delay": "{{ delay }}",
          "fwd-server-type": "fortianalyzer",
          "fwd-reliable": "{{ reliable }}",
          {% if peercn is defined %}
            "peer-cert-cn": "{{ peercn }}",
          {% endif %}
          "fwd-secure": "{{ secure }}"
      },
      "url": "/cli/global/system/log-forward"
    }
  ],
  "session": "{{ session }}",
  "id": 1
}
"""

DEL_FORWARDER = """
{
  "method": "delete",
  "params": [
    {
      "url": "/cli/global/system/log-forward/{{ id }}"
    }
  ],
  "session": "{{ session }}",
  "id": 1
}
"""
