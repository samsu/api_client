# Copyright (c) 2018 Fortinet, Inc.
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

# Namespace
# query
GET_NAMESPACE = """
{
    {% if id is defined %}
        "path": "/api/v1/namespace/{{ id }}/",
    {% else %}
        {% set _options = {
            "is_default": is_default,
            "name": name,
            "customer_id": customer_id
        } %}
        {% set _query = [] %}
        {% for k, v in _options.iteritems() if v is defined %}
            {% if _query.append('&'+k+'='+v) %}
            {% endif %}
        {% endfor %}
        {% if _query %}
            {% set _query = ''.join(_query) %}
            "path": "/api/v1/namespace/?{{ _query }}",
        {% else %}
            "path": "/api/v1/namespace/",
        {% endif %}
    {% endif %}
    "method": "GET"
}
"""

# add
ADD_NAMESPACE = """
{
    "path": "/api/v1/namespace",   
    "method": "POST",
    "body": {
        "name": "{{ name }}",
        "description": "{{ description }}"
    }
}
"""

# delete
DELETE_NAMESPACE = """
{
    "path": "/api/v1/namespace/{{ id }}/",
    "method": "DELETE"
}
"""


# Activation
# query
GET_ACTIVATION = """
{
    {% if id is defined %}
        "path": "/api/v1/activation/{{ id }}/",
    {% else %}
        {% set _options = {
            "sn": sn,
            "vdom": vdom,
            "namespace_id": namespace_id,
            "customer_id": customer_id
        } %}
        {% set _query = [] %}
        {% for k, v in _options.iteritems() if v is defined %}
            {% if _query.append('&'+k+'='+v) %}
            {% endif %}
        {% endfor %}
        {% if _query %}
            {% set _query = ''.join(_query) %}
            "path": "/api/v1/activation/?{{ _query }}",
        {% else %}
            "path": "/api/v1/activation/",
        {% endif %}
    {% endif %}
    "method": "GET"
}
"""

# add
ADD_ACTIVATION = """
{
    "path": "/api/v1/activation/",
    "method": "POST",
    "body": {
        "sn": "{{ sn }}",
        "vdom": "{{ vdom }}",     
        "namespace": "{{ namespace }}"
    }
}
"""


# delete
DELETE_ACTIVATION = """
{
    "path": "/api/v1/activation/{{ id }}/",
    "method": "DELETE"
}
"""


# count
GET_COUNT = """
{
    {% set _options = {
        "resource": resource,
        "namespace_id": namespace_id,
        "active": active,
        "customer_id": customer_id
    } %}
    {% set _query = [] %}
    {% for k, v in _options.iteritems() if v is defined %}
        {% if _query.append('&'+k+'='+v) %}
        {% endif %}
    {% endfor %}
    {% if _query %}
        {% set _query = ''.join(_query) %}
        "path": "/api/v1/count/?{{ _query }}",
    {% else %}
        "path": "/api/v1/count/",
    {% endif %}

    "method": "GET"
}
"""


# authentication
ADD_AUTH = """
{
    "path": "/api/v1/auth/",
    "method": "POST",
    "body": {
        "sn": "{{ sn }}",
        "namespace_id": "{{ namespace_id }}",     
        "username": "{{ username }}",
        {% if token is defined and token is not None %}
            "token": "{{ token }}"
        {% endif %}
    }
}
"""
