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


# usergroups
# query usergroups
GET_USERGROUPS = """
{
    {% if id is defined %}
        "path": "/api/v1/usergroups/{{ id }}/",
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

# delete an usergroup
DELETE_USERGROUP = """
{
    "path": "/api/v1/usergroups/",
    "method": "DELETE",
    "body": {
        "name": "{{ name }}"
    }
}
"""

## user
# query users
GET_USERS = """
{
    {% if id is defined %}
        "path": "/api/v1/localusers/{{ id }}/",
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
        {% for k, v in _options.iteritems() if v is defined and v %}
            {% if _query.append('&'+k+'='+v) %}
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

# create an user
CREATE_USER = """
{
    "path": "/api/v1/localusers/",
    "method": "POST",
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
        {% for k, v in _options.iteritems() if v is defined and v %}
            "{{ k }}": "{{ v }}",
        {% endfor %}
        "username": "{{ username }}"
    }
}
"""

# modify an user
MODIFY_USER = """
{
    "path": "/api/v1/localusers/{{ id }}/",
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
        {% for k, v in _options.iteritems() if v is defined and v %}
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

## FortiToken
# query FortiToken
GET_FORTITOKENS = """
{
    {% set _options = {
        "serial": serial,
        "status": status,
        "type": type
    } %}
    {% set _query = [] %}
    {% for k, v in _options.iteritems() if v is defined and v %}
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

# user authentication
CREATE_AUTH = """
{
    "path": "/api/v1/auth/",
    "method": "POST",
    "body": {
        {% if token_code is defined %}
            "token_code": "{{ token_code }}",
        {% endif %}
        {% if password is defined %}
            "password": "{{ password }}",
        {% endif %}
        "username": "{{ username }}"
    }
}
"""
