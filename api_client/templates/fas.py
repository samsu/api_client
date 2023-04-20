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

# Version
GET_VERSION = """
{
    {% if sn is defined %}
        "path": "/version?sn={{ sn }}",
    {% else %}
        "path": "/version/",
    {% endif %}    
    "method": "GET"
}
"""


# Namespace
# query
GET_REALM = """
{
    {% if id is defined %}
        {% if sn is defined %}
            "path": "/api/v1/realm/{{ id }}?sn={{ sn }}",
        {% else %}
            "path": "/api/v1/realm/{{ id }}/,
        {% endif %}
    {% else %}
        {% set _options = {
            "sn": sn,
            "is_default": is_default,
            "name": name,
            "customer_id": customer_id,
            "cluster_members": cluster_members
        } %}
        {% set _query = [] %}
        {% for k, v in _options.items() if v is defined %}
            {% if _query.append(k+'='+translate_uri_chars(v)) %}
            {% endif %}
        {% endfor %}
        {% if _query %}
            {% set _query = '&'.join(_query) %}
            "path": "/api/v1/realm?{{ _query }}",
        {% else %}
            "path": "/api/v1/realm/",
        {% endif %}
    {% endif %}
    "method": "GET"
}
"""

# add
ADD_REALM = """
{
    "path": "/api/v1/realm",   
    "method": "POST",
    "body": {
        {% if description is defined %}
            "description": "{{ description }}",
        {% endif %}
        {% if sn is defined %}
            "sn": "{{ sn }}",
        {% endif %}
        "name": "{{ name }}"
    }
}
"""

# delete
DELETE_REALM = """
{
    {% if sn is defined %}
        "path": "/api/v1/realm/{{ id }}?sn={{ sn }}",
    {% else %}
        "path": "/api/v1/realm/{{ id }}/,
    {% endif %}    
    "method": "DELETE"
}
"""


# authenticated api client
# query
GET_CLIENT = """
{
    {% if id is defined %}
        {% if sn is defined %}
            "path": "/api/v1/client/{{ id }}?sn={{ sn }}",
        {% else %}
            "path": "/api/v1/client/{{ id }}/,
        {% endif %}        
    {% else %}
        {% set _options = {
            "sn": sn,
            "vdom": vdom,
            "realm_id": realm_id,
            "customer_id": customer_id,
            "cluster_members": cluster_members
        } %}
        {% set _query = [] %}
        {% for k, v in _options.items() if v is defined %}
            {% if _query.append(k+'='+translate_uri_chars(v)) %}
            {% endif %}
        {% endfor %}
        {% if _query %}
            {% set _query = '&'.join(_query) %}
            "path": "/api/v1/client?{{ _query }}",
        {% else %}
            "path": "/api/v1/client/",
        {% endif %}
    {% endif %}
    "method": "GET"
}
"""


# delete
DELETE_CLIENT = """
{
    {% if sn is defined %}
        "path": "/api/v1/client/{{ id }}?sn={{ sn }}",
    {% else %}
        "path": "/api/v1/client/{{ id }}/,
    {% endif %}    
    "method": "DELETE"
}
"""


# User
# query
GET_USER = """
{
    {% if id is defined %}
        {% if sn is defined %}
            "path": "/api/v1/user/{{ id }}?sn={{ sn }}",
        {% else %}
            "path": "/api/v1/user/{{ id }}/,
        {% endif %}        
    {% else %}
        {% set _options = {
            "sn": sn,
            "username": username,
            "email": email,
            "mobile_number": mobile_number,
            "realm_id": realm_id,
            "realm": realm,
            "vdom": vdom,
            "active": active,
            "auth_method": auth_method,
            "notification_method": notification_method,
            "customer_id": customer_id,
            "cluster_members": cluster_members            
        } %}
        {% set _query = [] %}
        {% for k, v in _options.items() if v is defined %}
            {% if _query.append(k+'='+translate_uri_chars(v)) %}
            {% endif %}
        {% endfor %}        
        {% if _query %}
            {% set _query = '&'.join(_query) %}
            "path": "/api/v1/user?{{ _query }}",
        {% else %}
            "path": "/api/v1/user/",
        {% endif %}
    {% endif %}
    "method": "GET"
}
"""

# add
ADD_USER = """
{
    "path": "/api/v1/user/",
    "method": "POST",
    "body": {
        "sn": "{{ sn }}",
        "vdom": "{{ vdom }}",    
        "email": "{{ email }}",
        {% if realm_id is defined %}
            "realm_id": "{{ realm_id }}",
        {% elif realm is defined %}
            "realm": "{{ realm }}",
        {% endif %}
        {% if mobile_number is defined %}
            "mobile_number": "{{ mobile_number }}",         
        {% endif %}
        {% if auth_method is defined %}
            "auth_method": "{{ auth_method }}",         
        {% endif %}
        {% if notification_method is defined %}
            "notification_method": "{{ notification_method }}",         
        {% endif %}        
        {% if cluster_members is defined %}        
            "cluster_members": [
            {% for member in cluster_members %} 
                "{{ member }}"{{ "," if not loop.last }}
            {% endfor %}
            ],         
        {% endif %}
        "username": "{{ username }}"
    }
}
"""

# delete
DELETE_USER = """
{
    {% if cluster_members is defined %}
        {% set _members = translate_uri_chars(cluster_members) %}
        {% set _url = "/api/v1/user/" + id + "?cluster_members=" + _members %}
        {% if sn is defined %}
            "path": "{{ _url }}&sn={{ sn }}",
        {% else %}
            "path": "{{ _url }}",
        {% endif %}
    {% else %}
        {% if sn is defined %}
            "path": "/api/v1/user/{{ id }}?sn={{ sn }}",
        {% else %}
            "path": "/api/v1/user/{{ id }}/,
        {% endif %}
    {% endif %}
    "method": "DELETE"
}
"""

# put
MODIFY_USER = """
{
    "path": "/api/v1/user/{{ id }}/",
    "method": "PUT",
    "body": {
        {% set _options = {
        "sn": sn,        
        "email": email,
        "mobile_number": mobile_number,        
        "active": active,
        "change_token": change_token        
        } %}
        {% for k, v in _options.items() if v is defined %}
            "{{ k }}": "{{ v }}",
        {% endfor %}
        "id": "{{ id }}"
    }
}
"""

SYNC_USER = """
{
    "path": "/api/v1/user_sync/",
    "method": "POST",
    "body": {        
        {% if vdom is defined %}
            "vdom": "{{ vdom }}",
        {% endif %}
        {% if realm is defined %}
            "realm": "{{ realm }}",
        {% endif %}
        {% if users is defined %}
            "users": [
            {% for user in users %} 
                {{ user }}{{ "," if not loop.last }}
            {% endfor %}
            ],         
        {% endif %}
        {% if cluster_members is defined %}        
            "cluster_members": [
            {% for member in cluster_members %} 
                "{{ member }}"{{ "," if not loop.last }}
            {% endfor %}
            ],         
        {% endif %}
        "sn": "{{ sn }}"
}
"""


# count
GET_COUNT = """
{
    {% set _options = {
        "sn": sn,
        "resource": resource,
        "realm_id": realm_id,
        "active": active,
        "customer_id": customer_id,
        "cluster_members": cluster_members
    } %}
    {% set _query = [] %}
    {% for k, v in _options.items() if v is defined %}
        {% if _query.append(k+'='+translate_uri_chars(v)) %}
        {% endif %}
    {% endfor %}
    {% if _query %}
        {% set _query = '&'.join(_query) %}
        "path": "/api/v1/count?{{ _query }}",
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
        {% if token is defined %}
            "token": "{{ token }}",
        {% endif %}
        "sn": "{{ sn }}",
        "vdom": "{{ vdom }}",
        {% if realm_id is defined %}
            "realm_id": "{{ realm_id }}",
        {% elif realm is defined %}
            "realm": "{{ realm }}",
        {% endif %}
        {% if vdom is defined %}
            "vdom": "{{ vdom }}",
        {% endif %}
        {% if auth_method is defined %}
            "auth_method": "{{ auth_method }}",         
        {% endif %}   
        "username": "{{ username }}"
    }
}
"""


# statement
GET_STATEMENT = """
{
    {% set _options = {
        "sn": sn,
        "start": start,
        "end": end,
        "realm_id": realm_id,
        "realm": realm,
        "cluster_members": cluster_members
    } %}
    {% set _query = [] %}
    {% for k, v in _options.items() if v is defined %}
        {% if _query.append(k+'='+translate_uri_chars(v)) %}
        {% endif %}
    {% endfor %}
    {% if _query %}
        {% set _query = '&'.join(_query) %}
        "path": "/api/v1/statement?{{ _query }}",
    {% else %}
        "path": "/api/v1/statement/",
    {% endif %}

    "method": "GET"
}
"""

# token activation
ADD_TOKEN_ACTIVATION = """
{
    "path": "/api/v1/token/activation",
    "method": "POST",
    "body": {        
        {% if token is defined %}
            "token": "{{ token }}",
        {% endif %}    
    }
}
"""

TOKEN_TRANSFER_START = """
{
    "path": "/api/v1/token/transfer/start",
    "method": "POST",
    "body": {
        "sn": "{{ sn }}",      
        "tokens": "{{ tokens }}",
        "reg_id": "{{ reg_id }}",
        "hmac": "{{ hmac }}",
        "transfer_code": "{{ transfer_code }}",
        "msg_sn": "FortiToken Cloud"
    }
}
"""

# Trial
ADD_TRIAL = """
{
    "path": "/api/v1/trial/",
    "method": "POST",
    "body": {
        "sn": "{{ sn }}"
    }
}
"""

# authenticated api client
# query
GET_TASK = """
{
    {% if id is defined %}        
        {% set _options = {
            "sn": sn,
            "vdom": vdom,
            "realm_id": realm_id,
            "customer_id": customer_id,
            "cluster_members": cluster_members
        } %}
        {% set _query = [] %}
        {% for k, v in _options.items() if v is defined %}
            {% if _query.append(k+'='+translate_uri_chars(v)) %}
            {% endif %}
        {% endfor %}
        {% if _query %}
            {% set _query = '&'.join(_query) %}
            "path": "/api/v1/task/{{ id }}?{{ _query }}",
        {% else %}
            "path": "/api/v1/task/{{ id }}",
        {% endif %}
    {% endif %}
    "method": "GET"
}
"""

GET_COUNT_AUTH = """
{
    "path": "/faas_auth*/_search?pretty",
    "method": "GET",
    "body": {
        "query": {
            "range": {
                "@timestamp": {
                    "gte": "now-7d",
                    "lte": "now"
                }
            }
        },
        "aggs": {
            "auth_by_customer_id": {
                "terms": {
                    "field": "context.customer_id.keyword",
                    "size": 50
                }
            }
        }
    }
}
"""

GET_OPENID_CONFIGURATION = """
{
    "path": "/api/v1/.well-known/openid-configuration",
    "method": "GET"
}
"""
