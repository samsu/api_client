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

#    FortiAuthenticator API request format templates.

# About api request message naming regulations:
# Prefix         HTTP method
# ADD_XXX      -->    POST
# SET_XXX      -->    PUT
# DELETE_XXX   -->    DELETE
# GET_XXX      -->    GET
# MODIFY_XXX   -->    PATCH


# METADATA
# query METADATA
GET_METADATA = """
{
    "path": "/saml-idp/{{ prefix }}/metadata/",
    "method": "GET"
}
"""

# usergroups
# query usergroups
GET_USERGROUPS = """
{
    {% if id is defined %}
        "path": "/api/v1/usergroups/{{ id }}/",
    {% elif resource_uri is defined %}
        "path": "{{ resource_uri }}",
    {% else %}
        {% if name is defined %}
            "path": "/api/v1/usergroups/?name={{ name }}",
        {% else %}
            "path": "/api/v1/usergroups/",
        {% endif %}
    {% endif %}
    "method": "GET"
}
"""

GET_USERGROUP = GET_USERGROUPS

# create an usergroup
CREATE_USERGROUP = """
{
    "path": "/api/v1/usergroups/",
    "method": "POST",
    "body": {
        "name": "{{ name }}"
    }
}
"""

# modify an usergroup
MODIFY_USERGROUP = """
{
    "path": "/api/v1/usergroups/{{ id }}/",
    "method": "PATCH",
     "body": {
        {% if users is defined %}
            "users": ["{{ users }}"]
        {% endif %}
     }
}
"""

# delete an usergroup
DELETE_USERGROUP = """
{
    {% if id is defined %}
        "path": "/api/v1/usergroups/{{ id }}/",
    {% elif resource_uri is defined %}
        "path": "{{ resource_uri }}",
    {% endif %}
    "method": "DELETE"
}
"""

# user
# query users
GET_USERS = """
{
    {% if id is defined %}
        "path": "/api/v1/localusers/{{ translate_uri_chars(id) }}/",
    {% else %}
        {% set _options = {
            "username": username,
            "token_auth": token_auth,
            "ftk_only": ftk_only,
            "ftm_act_method": ftm_act_method,
            "token_type": token_type,
            "token_serial": token_serial,
            "first_name": first_name,
            "last_name": last_name,
            "user_groups": user_groups,
            "address": address,
            "city": city,
            "state": state,
            "country": country,
            "email": email,
            "mobile_number": mobile_number,
            "phone_number": phone_number,
            "expires_at": expires_at,
            "custom1": custom1,
            "custom2": custom2,
            "custom3": custom3,
            "active": active
        } %}
        {% set _query = [] %}
        {% for k, v in _options.items() if v is defined %}
            {% if _query.append('&'+k+'='+translate_uri_chars(v)) %}
            {% endif %}
        {% endfor %}
        {% if _query %}
            {% set _query = ''.join(_query) %}
            "path": "/api/v1/localusers/?{{ _query }}",
        {% else %}
            "path": "/api/v1/localusers/",
        {% endif %}
    {% endif %}
    "method": "GET"
}
"""

GET_USER = GET_USERS


# create an user
CREATE_USER = """
{
    "path": "/api/v1/localusers/",
    "method": "POST",
    "body": {
        {%
            set _options = {
                "token_auth": token_auth,
                "password": password,
                "ftk_only": ftk_only,
                "ftm_act_method": ftm_act_method,
                "token_type": token_type,
                "token_serial": token_serial,
                "first_name": first_name,
                "last_name": last_name,
                "address": address,
                "city": city,
                "state": state,
                "country": country,
                "email": email,
                "mobile_number": mobile_number,
                "phone_number": phone_number,
                "expires_at": expires_at,
                "custom1": custom1,
                "custom2": custom2,
                "custom3": custom3,
                "active": active
            }
        %}
        {% if user_groups is defined %}
            "user_groups": ["{{ user_groups }}"],
        {% endif %}
        {% for k, v in _options.items() if v is defined %}
            "{{ k }}": "{{ v }}",
        {% endfor %}
        "username": "{{ username }}"
    }
}
"""

# modify an user
MODIFY_USER = """
{
    "path": "/api/v1/localusers/{{ translate_uri_chars(id) }}/",
    "method": "PATCH",
    "body": {
        {%
            set _options = {
                "token_auth": token_auth,
                "ftk_only": ftk_only,
                "ftm_act_method": ftm_act_method,
                "token_type": token_type,
                "token_serial": token_serial,
                "first_name": first_name,
                "last_name": last_name,
                "user_groups": user_groups,
                "address": address,
                "city": city,
                "state": state,
                "country": country,
                "email": email,
                "mobile_number": mobile_number,
                "phone_number": phone_number,
                "expires_at": expires_at,
                "custom1": custom1,
                "custom2": custom2,
                "custom3": custom3,
                "active": active
            }
        %}
        {% for k, v in _options.items() if v is defined %}
            "{{ k }}": "{{ v }}",
        {% endfor %}
        "id": {{ id }}
    }
}
"""

# delete an usergroup
DELETE_USER = """
{
    "path": "/api/v1/localusers/{{ id }}/",
    "method": "DELETE"
}
"""

# FortiToken
# query FortiToken
GET_FORTITOKENS = """
{
    {% set _options = {
        "serial": serial,
        "status": status,
        "type": type,
        "limit": limit
    } %}
    {% set _query = [] %}
    {% for k, v in _options.items() if v is defined %}
        {% if _query.append('&'+k+'='+v) %}
        {% endif %}
    {% endfor %}
    {% if _query %}
        {% set _query = ''.join(_query) %}
        {% set _query = '?' + _query[1:] %}
        "path": "/api/v1/fortitokens/{{ _query }}",
    {% else %}
        "path": "/api/v1/fortitokens/",
    {% endif %}
    "method": "GET"
}
"""

GET_FORTITOKEN = GET_FORTITOKENS


# authentication
# user authentication either with token_code or with password
CREATE_AUTH = """
{
    "path": "/api/v1/auth/",
    "method": "POST",
    "body": {
        {% if token_code is defined %}
            "token_code": "{{ token_code }}",
        {% else %}
            {% if display_name is defined %}
                "display_name": "{{ display_name }}",
            {% endif %}
        {% endif %}
        {% if password is defined %}
            "password": "{{ password }}",
        {% endif %}
        "username": "{{ username }}"
    }
}
"""

# user push authentication
CREATE_PUSHAUTH = """
{
    "path": "/api/v1/pushauth/",
    "method": "POST",
    "body": {
        {%
            set _options = {
                "realm": realm,
                "user_ip": user_ip,
                "timestamp": timestamp,
                "account": account,
                "user_agent": user_agent,
                "display_name": display_name,
                "user_data": user_data,
                "log_message": log_message
            }
        %}
        {% for k, v in _options.items() if v is defined %}
            "{{ k }}": "{{ v }}",
        {% endfor %}
        "username": "{{ username }}"
    }
}
"""

CREATE_PUSHAUTHRESP = """
{
    "path": "/api/v1/pushauthresp/",
    "method": "POST",
    "body": {
        {%
            set _options = {
                "token_code": token_code,
                "session_id": session_id,
                "message": message,
                "hmac": hmac
            }
        %}
        {% for k, v in _options.items() if v is defined %}
            "{{ k }}": "{{ v }}",
        {% endfor %}
        "action": "{{ action }}"
    }
}
"""

GET_FTMLICENSE = """
{
    "path": "/api/v1/fortitokenmobilelicenses/",
    "method": "GET"
}
"""

UPLOAD_FTMLICENSE = """
{
    "path": "/api/v1/fortitokenmobilelicenses/",
    "method": "POST",
    "body": {
        "license": "{{ license }}"
    }
}
"""

GET_SMTPSERVER = """
{
    {% if id is defined %}
    "path": "/api/v1/smtpservers/{{ id }}/",
    {% else %}
    "path": "/api/v1/smtpservers/",
    {% endif %}
    "method": "GET"
}
"""

CREATE_SMTPSERVER = """
{
    "path": "/api/v1/smtpservers/",
    "method": "POST",
    "body": {
        "sender_email": "{{ sender_email }}",
        "address": "{{ address }}",
        {%
            set _options = {
                "default": default,
                "sender_name": sender_name,
                "secure": secure,
                "authentication_name": authentication_name,
                "authentication_password": authentication_password,
                "port": port,
                "authentication": authentication
            }
        %}
        {% for k, v in _options.items() if v is defined %}
            "{{ k }}": "{{ v }}",
        {% endfor %}

        "name": "{{ name }}"
    }
}
"""

MODIFY_SMTPSERVER = """
{
    "path": "/api/v1/smtpservers/{{ id }}/",
    "method": "PATCH",
    "body": {
        {%
            set _options = {
                "name": name,
                "default": default,
                "sender_email": sender_email,
                "sender_name": sender_name,
                "address": address,
                "secure": secure,
                "authentication_name": authentication_name,
                "authentication_password": authentication_password,
                "port": port,
                "authentication": authentication
            }
        %}
        {% for k, v in _options.items() if v is defined %}
            "{{ k }}": "{{ v }}"
            {{ "," if not loop.last }}
        {% endfor %}
    }
}

"""

DELETE_SMTPSERVER = """
{
    "path": "/api/v1/smtpservers/{{ id }}/",
    "method": "DELETE"
}
"""

GET_USERLOCKOUTPOLICY = """
{
    "path": "/api/v1/userlockoutpolicy/",
    "method": "GET"
}
"""

MODIFY_USERLOCKOUTPOLICY = """
{
    "path": "/api/v1/userlockoutpolicy/",
    "method": "PATCH",
    "body": {
        {%
            set _options = {
                "failed_login_lockout": lockout,
                "failed_login_lockout_max_attempts": max_attempts,
                "failed_login_lockout_permanent": permanent,
                "failed_login_lockout_period": period,
                "inactivity_lockout": inactivity_lockout,
                "inactivity_lockout_period": inactivity_lockout_period
            }
        %}
         {% for k, v in _options.items() if v is defined %}
            "{{ k }}": {{ v }}
            {{ "," if not loop.last }}
        {% endfor %}

    }
}
"""

GET_FTMFQDN = """
{
    "path": "/api/v1/system/external_ip_fqdn/",
    "method": "GET"
}
"""

MODIFY_FTMFQDN = """
{
    "path": "/api/v1/system/external_ip_fqdn/",
    "method": "PUT",
    "body": {
        "value": "{{ fqdn }}"
    }
}
"""

GET_FTMTOKENS = """
{
    {% if ftm_license is defined %}
    "path": "/api/v1/fortitokens/?type=ftm&license={{ ftm_license }}",
    {% else %}
    "path": "/api/v1/fortitokens/?type=ftm",
    {% endif %}
    "method": "GET"
}
"""

DELETE_FTMTOKENS = """
{
    "path": "{{ resource_uri }}",
    "method": "DELETE"
}
"""

GET_SYSTEMINFO = """
{
    "path": "/api/v1/systeminfo/",
    "method": "GET"
}
"""

GET_FTPSERVERS = """
{
    {% if id is defined %}
        "path": "/api/v1/ftpservers/{{ translate_uri_chars(id) }}/",
    {% else %}
        "path": "/api/v1/ftpservers/",
    {% endif %}
    "method": "GET"
}
"""

CREATE_FTPSERVER = """
{
    "path": "/api/v1/ftpservers/",
    "method": "POST",
    "body": {
        {%
            set _options = {
                "username": username,
                "password": password,
                "anonymous": anonymous
            }
        %}
        {% for k, v in _options.items() if v is defined %}
            "{{ k }}": "{{ v }}",
        {% endfor %}
        "name": "{{ name }}",
        "address": "{{ address  }}",
        "port": {{ port }},
        "conn_type": "{{ conn_type }}"
    }
}
"""

MODIFY_FTPSERVER = """
{
    "path": "/api/v1/ftpservers/{{ id }}/",
    "method": "PATCH",
    "body": {
        {%
            set _options = {
                "username": username,
                "password": password,
                "anonymous": anonymous,
                "name": name,
                "address": address,
                "conn_type": conn_type,
                "port": port
            }
        %}
        {% for k, v in _options.items() if v is defined %}
            "{{ k }}": "{{ v }}"
            {{ "," if not loop.last }}
        {% endfor %}
    }
}
"""

DELETE_FTPSERVER = """
{
    "path": "/api/v1/ftpservers/{{ id }}/",
    "method": "DELETE"
}
"""

GET_SCHEDULED_BACKUP_SETTING = """
{
    "path": "/api/v1/scheduledbackupsettings/",
    "method": "GET"
}
"""

CREATE_SCHEDULED_BACKUP_SETTING = """
{
    "path": "/api/v1/scheduledbackupsettings/",
    "method": "POST",
    "body": {
        {%
            set _options = {
                "directory": directory,
                "ftp": ftp,
                "ftp_2": ftp_2,
                "frequency": frequency,
                "time": time,
                "encryption_password": encryption_password
            }
        %}
        {% for k, v in _options.items() if v is defined %}
            "{{ k }}": "{{ v }}",
        {% endfor %}
        {% if encryption_enabled is defined %}
            "encryption_enabled": {{ encryption_enabled }},
        {% endif %}
        "enabled": "{{ enabled }}"
    }
}
"""

MODIFY_SCHEDULED_BACKUP_SETTING = """
{
    "path": "/api/v1/scheduledbackupsettings/",
    "method": "PATCH",
    "body": {
        {%
            set _options = {
                "directory": directory,
                "ftp": ftp,
                "ftp_2": ftp_2,
                "frequency": frequency,
                "time": time,
                "encryption_password": encryption_password
            }
        %}
        {% for k, v in _options.items() if v is defined %}
            "{{ k }}": "{{ v }}",
        {% endfor %}
        {% if encryption_enabled is defined %}
            "encryption_enabled": {{ encryption_enabled }},
        {% endif %}
        "enabled": "{{ enabled }}"
    }
}
"""

#  v6.3.0
BACKUP_CONFIG = """
{
    "path": "/api/v1/recovery/",
    "method": "GET",
    "body": {
        {% if key is defined %}
            "key": "{{ key }}"
        {% endif %}
    }
}
"""

RESTORE_CONFIG = """
{
    "path": "/api/v1/recovery/",
    "method": "POST"
}
"""

UPLOAD_LICENSE = """
{
    "path": "/api/v1/licensing/",
    "method": "POST"
}
"""

UPGRADE_FIRMWARE = """
{
    "path": "/api/v1/upgrade/",
    "method": "POST"
}
"""

GET_SNMP_SETTING = """
{
    "path": "/api/v1/snmpgeneral/",
    "method": "GET"
}
"""

MODIFY_SNMP_SETTING = """
{
    "path": "/api/v1/snmpgeneral/",
    "method": "PATCH",
    "body": {
        {%
            set _options = {
                "contact": contact,
                "decription": description,
                "location": location,
                "users": users,
                "groups": groups,
                "radius_clients": radius_client,
                "tacplus_clients": tacplus_client,
                "auth_events": auth_events,
                "auth_failures": auth_failures,
                "cpu": cpu,
                "memory": memory,
                "disk": disk,
            }
        %}
        {% for k, v in _options.items() if v is defined %}
            "{{ k }}": "{{ v }}"
            {{ "," if not loop.last }}
        {% endfor %}
    }
}
"""

GET_SNMP_COMMUNITIES = """
{
    {% if id is defined %}
        "path": "/api/v1/snmp/{{ id }}/",
    {% else %}
        "path": "/api/v1/snmp/",
    {% endif %}
    "method": "GET"
}
"""

CREATE_SNMP_COMMUNITY = """
{
    "path": "/api/v1/snmp/",
    "method": "POST",
    "body": {
        {%
            set _options = {
                "cpu": cpu,
                "memory": memory,
                "disk": disk,
                "interface_ip": interface_ip,
                "users": users,
                "groups": groups,
                "radius_clients": radius_clients,
                "tacplus_clients": tacplus_clients,
                "auth_events": auth_events,
                "auth_failures": auth_failures,
                "user_lockout": user_lockout,
                "ha_status": ha_status,
                "ha_sync": ha_sync,
                "raid": raid,
            }
        %}
        {% for k, v in _options.items() if v is defined %}
            "{{ k }}": {{ v }},
        {% endfor %}
        "name": "{{ name }}"
    }
}
"""

MODIFY_SNMP_COMMUNITY = """
{
    "path": "/api/v1/snmp/{{ id }}/",
    "method": "PATCH",
    "body": {
        {%
            set _options = {
                "cpu": cpu,
                "memory": memory,
                "disk": disk,
                "interface_ip": interface_ip,
                "users": users,
                "groups": groups,
                "radius_clients": radius_clients,
                "tacplus_clients": tacplus_clients,
                "auth_events": auth_events,
                "auth_failures": auth_failures,
                "user_lockout": user_lockout,
                "ha_status": ha_status,
                "ha_sync": ha_sync,
                "raid": raid,
            }
        %}
        {% for k, v in _options.items() if v is defined %}
            "{{ k }}": {{ v }}
            {{ "," if not loop.last }}
        {% endfor %}
    }
}
"""

DELETE_SNMP_COMMUNITY = """
{
    "path": "/api/v1/snmp/{{ id }}/",
    "method": "DELETE"
}
"""

GET_SNMP_COMMUNITY_HOSTS = """
{
    {% if hid is defined %}
        "path": "/api/v1/snmp/{{ id }}/hosts//{{ hid }}/",
    {% else %}
        "path": "/api/v1/snmp/{{ id }}/hosts/",
    {% endif %}
    "method": "GET"
}
"""

CREATE_SNMP_COMMUNITY_HOST = """
{
    "path": "/api/v1/snmp/{{ id }}/hosts/",
    "method": "POST",
    "body": {
        {%
            set _options = {
                "query": query,
                "trap": trap,
            }
        %}
        {% for k, v in _options.items() if v is defined %}
            "{{ k }}": "{{ v }}",
        {% endfor %}
        "address": "{{ address }}"
    }
}
"""

MODIFY_SNMP_COMMUNITY_HOST = """
{
    "path": "/api/v1/snmp/{{ id }}/hosts/{{ hid }}/",
    "method": "PATCH",
    "body": {
        {%
            set _options = {
                "query": query,
                "trap": trap,
                "address": address,
            }
        %}
        {% for k, v in _options.items() if v is defined %}
            "{{ k }}": "{{ v }}"
            {{ "," if not loop.last }}
        {% endfor %}
    }
}
"""

DELETE_SNMP_COMMUNITY_HOST = """
{
    "path": "/api/v1/snmp/{{ id }}/hosts/{{ hid }}/",
    "method": "DELETE"
}
"""
