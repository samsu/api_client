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

LOGIN = """
{
    "path": "/XX/YY/ZZ/AUTH",
    "method": "POST",
    "body": "magic=175805987&username={{ username }}&password={{ password }}&4Tredir=%2F&4Tmthd=0&domain=local"
}
"""

REDIRECT = """
{
    "path": "{{ path }}",
    "method": "GET"
}
"""

LOGOUT = """
{
    "path": "/logout?",
    "method": "GET"
}
"""

CREATE_SECRET = """
{
    "path": "/api/v2/cmdb/secret/database",
    "method": "POST",
    "body": {
        {% if ( (folder is defined and inherit_permission is defined) and
                (inherit_permission == "enable") ) %}
            "folder": {{ folder }},
            "inherit-permission": "enable",
        {% else %}
            "id": {{ id | default(0) }},
            "checkout-user": "{{ checkout_user | default("") }}",
            "pwd-chg-use-policy-default": "{{ pwd_chg_use_policy_default | default("enable") }}",
            "heartbeat-use-policy-default": "{{ heartbeat_use_policy_default | default("enable") }}",
            "folder": {{ folder | default(1) }},
            "associated-secret": {{ associated_secret | default(0) }},
            "ssh-connect-with": "{{ ssh_connect_with | default("self") }}",
            "ssh-auto-password": "{{ ssh_auto_password | default("disable") }}",
            "ztna-tags-match-logic": "{{ ztna_tags_match_logic | default("or") }}",
            "rsa-sign-algo": "{{ rsa_sign_algo | default("ssh-rsa") }}",
            "keyboard-layout": "{{ keyboard_layout | default("en-us") }}",
            "description": "{{ description | default("") }}",
            "inherit-permission": "{{ inherit_permission | default("enable") }}",
            "ztna-ems-tag": {{ ztna_ems_tag | default([]) }},
            "user-permission": {{ user_permission | default([]) }},
            "group-permission": {{ group_permission | default([]) }},
            "ssh-service-status": "{{ ssh_service_status | default("up") }}",
            "ssh-service-port": {{ ssh_service_port | default(0) }},
            "rdp-service-status": "{{ rdp_service_status | default("up") }}",
            "rdp-service-port": {{ rdp_service_port | default(0) }},
            "vnc-service-status": "{{ vnc_service_status | default("down") }}",
            "vnc-service-port": {{ vnc_service_port | default(0) }},
            "ldaps-service-status": "{{ ldaps_service_status | default("down") }}",
            "ldaps-service-port": {{ ldaps_service_port | default(0) }},
            "samba-service-status": "{{ samba_service_status | default("down") }}",
            "samba-service-port": {{ samba_service_port | default(0) }},
            "password-changer": "{{ password_changer | default("disable") }}",
            "password-heartbeat": "{{ password_heartbeat | default("disable") }}",
            "checkout": "{{ checkout | default("disable") }}",
            "recording": "{{ recording | default("disable") }}",
            "need-approval": "{{ need_approval | default("disable") }}",
            "need-approval-job": "{{ need_approval_job | default("disable") }}",
            "proxy": "{{ proxy | default("enable") }}",
            "ssh-filter": "{{ ssh_filter | default("disable") }}",
            "av-scan": "{{ av_scan | default("disable") }}",
            "rdp-security-level": "{{ rdp_security_level | default("best-effort") }}",
            "rdp-restricted-admin-mode": "{{ rdp_restricted_admin_mode | default("disable") }}",
            "block-rdp-clipboard": "{{ block_rdp_clipboard | default("disable") }}",
            "heartbeat-interval": {{ heartbeat_interval | default(60) }},
            "heartbeat-start-time": "{{ heartbeat_start_time | default("") }}",
            "checkout-duration": {{ checkout_duration | default(30) }},
            "checkin-pwd-change": "{{ checkin_pwd_change | default("disable") }}",
            "checkout-duration-renew": "{{ checkout_duration_renew | default("disable") }}",
            "checkout-renew-times": {{ checkout_renew_times | default(1) }},
            "tunnel-encryption": "{{ tunnel_encryption | default("disable") }}",
            "approval-profile": "{{ approval_profile | default("") }}",
            "ssh-filter-profile": "{{ ssh_filter_profile | default("") }}",
            "av-profile": "{{ av_profile | default("") }}",
        {% endif %}
        "name": "{{ name }}",
        "template": "{{ secret_template | default("Unix Account (SSH Password)") }}",
        "field": [
            {
                "id": 1,
                "name": "Host",
                "value": "{{ host | default("1.1.1.1") }}"
            },
            {
                "id": 2,
                "name": "Username",
                "value": "{{ username | default("1") }}"
            },
            {
                "id": 3,
                "name": "Password",
                "value": "{{ password | default("1") }}"
            },
            {
                "id": 4,
                "name": "URL",
                "value": "{{ url | default("") }}"
            }
        ]
    }
}
"""

GET_SECRETS = """
{
    "path": "/api/v2/cmdb/secret/database",
    "method": "GET",
    "body": {
        "json_filter": []
    }
}
"""

DELETE_SECRET = """
{
    "path": "/api/v2/cmdb/secret/database/{{ id }}",
    "method": "DELETE"
}
"""

CREATE_FOLDER = """
{
    "path": "/api/v2/cmdb/secret/folder",
    "method": "POST",
    "body": {
        "id": {{ id | default(0) }},
        "name": "{{ name | default("Auto_folder")}}",
        "parent-folder": {{ parent_folder | default(0) }},
        "secret-policy": "{{ secret_policy | default("default") }}",
        "inherit-policy": "{{ inherit_policy | default("disable") }}",
        "inherit-permission": "{{ inherit_permission | default("disable") }}",
        "user-permission": [
            {
                "id": 1,
                "folder-permission": "owner",
                "secret-permission": "owner",
                "user-name": [
                    {
                        "name": "admin",
                        "q_origin_key": "admin"
                    }
                ]
            }
        ],
        "group-permission": []
    }
}
"""

GET_FOLDERS = """
{
    "path": "/api/v2/cmdb/secret/folder",
    "method": "GET",
    "body": {
        "json_filter": []
    }
}
"""

DELETE_FOLDER = """
{
    "path": "/api/v2/cmdb/secret/folder/{{ id }}",
    "method": "DELETE"
}
"""
