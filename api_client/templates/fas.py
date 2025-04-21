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

# Login
LOGIN = """
{
    "path": "/api/v1/login/",
    "method": "POST",
    "body": {
        "client_id": "{{ client_id }}",
        "client_secret": "{{ client_secret }}"
    }
}
"""

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

# Customer
# query
GET_CUSTOMER = """
{
    {% if path is defined %}
        "path": "{{ path }}",
    {% else %}
        {% if ver is defined %}
            {% set _ver = ver %}
        {% else %}
            {% set _ver = 'v1' %}
        {% endif %}
        {% if id is defined %}
            {% if sn is defined %}
                "path": "/api/{{ _ver }}/customer/{{ id }}?sn={{ sn }}",
            {% else %}
                "path": "/api/{{ _ver }}/customer/{{ id }}/",
            {% endif %}
        {% else %}
            {% set _options = {
                "resource": resource,
                "start": start,
                "end": end,
                "expired": expired,
                "customer_id": customer_id,
                "user_email": user_email,
                "trial_status": trial_status,
                "disabled": disabled,
                "bypass": bypass,
                "license_type": license_type,
                "sn": sn,
                "expire_date": expire_date,
                "min_balance": min_balance,
                "max_balance": max_balance,
                "limit": limit,
                "next": next
            } %}
            {% set _query = [] %}
            {% for k, v in _options.items() if v is defined %}
                {% if _query.append(k+'='+translate_uri_chars(v)) %}
                {% endif %}
            {% endfor %}
            {% if _query %}
                {% set _query = '&'.join(_query) %}
                "path": "/api/{{ _ver }}/customer?{{ _query }}",
            {% else %}
                "path": "/api/{{ _ver }}/customer",
            {% endif %}
        {% endif %}
    {% endif %}
    "method": "GET"
}
"""

# put
MODIFY_CUSTOMER = """
{
    "path": "/api/v1/customer/{{ id }}/",
    "method": "PUT",
    "body": {
        {% set _options = {
        "status": status,
        "license_type": license_type,
        "bypass": bypass
        } %}
        {% for k, v in _options.items() if v is defined %}
            "{{ k }}": "{{ v }}",
        {% endfor %}
        "id": "{{ id }}"
    }
}
"""

# Realm
# query
GET_REALM = """
{
    {% if path is defined %}
        "path": "{{ path }}",
    {% else %}
        {% if ver is defined %}
            {% set _ver = ver %}
        {% else %}
            {% set _ver = 'v1' %}
        {% endif %}
        {% if id is defined %}
            {% if sn is defined %}
                "path": "/api/{{ _ver }}/realm/{{ id }}?sn={{ sn }}",
            {% else %}
                "path": "/api/{{ _ver }}/realm/{{ id }}/",
            {% endif %}
        {% else %}
            {% set _options = {
                "sn": sn,
                "is_default": is_default,
                "name": name,
                "customer_id": customer_id,
                "cluster_members": cluster_members,
                "limit": limit,
                "next": next
            } %}
            {% set _query = [] %}
            {% for k, v in _options.items() if v is defined %}
                {% if _query.append(k+'='+translate_uri_chars(v)) %}
                {% endif %}
            {% endfor %}
            {% if _query %}
                {% set _query = '&'.join(_query) %}
                "path": "/api/{{ _ver }}/realm?{{ _query }}",
            {% else %}
                "path": "/api/{{ _ver }}/realm",
            {% endif %}
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

# auth api client
# query
GET_CLIENT = """
{
    {% if path is defined %}
        "path": "{{ path }}",
    {% else %}
        {% if ver is defined %}
            {% set _ver = ver %}
        {% else %}
            {% set _ver = 'v1' %}
        {% endif %}
        {% if id is defined %}
            {% if sn is defined %}
                "path": "/api/{{ _ver }}/client/{{ id }}?sn={{ sn }}",
            {% else %}
                "path": "/api/{{ _ver }}/client/{{ id }}/",
            {% endif %}
        {% else %}
            {% set _options = {
                "sn": sn,
                "vdom": vdom,
                "realm_id": realm_id,
                "customer_id": customer_id,
                "cluster_members": cluster_members,
                "limit": limit,
                "next": next
            } %}
            {% set _query = [] %}
            {% for k, v in _options.items() if v is defined %}
                {% if _query.append(k+'='+translate_uri_chars(v)) %}
                {% endif %}
            {% endfor %}
            {% if _query %}
                {% set _query = '&'.join(_query) %}
                "path": "/api/{{ _ver }}/client?{{ _query }}",
            {% else %}
                "path": "/api/{{ _ver }}/client/",
            {% endif %}
        {% endif %}
    {% endif %}
    "method": "GET"
}
"""

# add
ADD_CLIENT = """
{
    "path": "/api/v1/client/",
    "method": "POST",
    "body": {
        {% set _options = {
        "sn": sn,
        "vdom": vdom,
        "vdoms": vdoms,
        "name": name,
        "realm_id": realm_id,
        "profile_id": profile_id,
        "permission": permission,
        "scope": scope,
        "realms": realms
        } %}
        {% set _int = ("permission", ) %}
        {% for k, v in _options.items() if v is defined %}
            {% if k not in _int %}
                "{{ k }}": "{{ v }}"{{ "," if not loop.last }}
            {% else %}
                "{{ k }}": {{ v }}{{ "," if not loop.last }}
            {% endif %}
        {% endfor %}
    }
}
"""

# modify
MODIFY_CLIENT = """
{
    "path": "/api/v1/client/{{ id }}/",
    "method": "PUT",
    "body": {
        {% set _options = {
        "sn": sn,
        "vdom": vdom,
        "name": name,
        "realm_id": realm_id,
        "profile_id": profile_id,
        "permission": permission,
        "scope": scope,
        "realms": realms
        } %}
        {% for k, v in _options.items() if v is defined %}
            "{{ k }}": "{{ v }}"{{ "," if not loop.last }}
        {% endfor %}
    }
}
"""

# delete
DELETE_CLIENT = """
{
    {% if sn is defined %}
        "path": "/api/v1/client/{{ id }}?sn={{ sn }}",
    {% else %}
        "path": "/api/v1/client/{{ id }}/",
    {% endif %}
    "method": "DELETE"
}
"""

# User
# query
GET_USER = """
{
    {% if path is defined %}
        "path": "{{ path }}",
    {% else %}
        {% if ver is defined %}
            {% set _ver = ver %}
        {% else %}
            {% set _ver = 'v1' %}
        {% endif %}
        {% if id is defined %}
            {% if sn is defined %}
                "path": "/api/{{ _ver }}/user/{{ id }}?sn={{ sn }}",
            {% else %}
                "path": "/api/{{ _ver }}/user/{{ id }}/",
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
                "cluster_members": cluster_members,
                "user_data": user_data,
                "limit": limit,
                "next": next
            } %}
            {% set _query = [] %}
            {% for k, v in _options.items() if v is defined %}
                {% if _query.append(k+'='+translate_uri_chars(v)) %}
                {% endif %}
            {% endfor %}
            {% if _query %}
                {% set _query = '&'.join(_query) %}
                "path": "/api/{{ _ver }}/user?{{ _query }}",
            {% else %}
                "path": "/api/{{ _ver }}/user/",
            {% endif %}
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
            "path": "/api/v1/user/{{ id }}/",
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

MODIFY_USERS = """
{
{% if path is defined %}
        "path": "{{ path }}",
    {% else %}
        {% if ver is defined %}
            {% set _ver = ver %}
        {% else %}
            {% set _ver = 'v1' %}
        {% endif %}
        {% if id is defined %}
            "path": "/api/{{ _ver }}/user/{{ id }}",
        {% else %}
            {% set _options = {
                "sn": filter_sn,
                "vdom": filter_vdom,
                "client_id": filter_client_id,
                "username": filter_username,
                "email": filter_email,
                "mobile_number": filter_mobile_number,
                "realm_id": filter_realm_id,
                "realm": filter_realm,
                "active": filter_active,
                "user_data": filter_user_data,
                "auth_method": filter_auth_method,
                "notification_method": filter_notification_method,
                "customer_id": filter_customer_id,
                "cluster_members": filter_cluster_members
            } %}
            {% set _query = [] %}
            {% for k, v in _options.items() if v is defined %}
                {% if _query.append(k+'='+translate_uri_chars(v)) %}
                {% endif %}
            {% endfor %}
            {% if _query %}
                {% set _query = '&'.join(_query) %}
                "path": "/api/{{ _ver }}/user?{{ _query }}",
            {% else %}
                "path": "/api/{{ _ver }}/user/",
            {% endif %}
        {% endif %}
    {% endif %}
    "method": "PUT",
    "body": {
        {% set _options = {
        "id": id,
        "sn": sn,
        "vdom": vdom,
        "client_id": client_id,
        "email": email,
        "mobile_number": mobile_number,
        "active": active,
        "user_data": user_data,
        "change_token": change_token
        } %}
        {% for k, v in _options.items() if v is defined %}
            "{{ k }}": "{{ v }}"{{ "," if not loop.last }}
        {% endfor %}
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

# token
GET_TOKEN = """
{
    "path":  "/api/v1/token/",
    {% set _options = {
        "token_sn": token_sn,
        "soft_token": soft_token
    } %}
    {% set _query = [] %}
    {% for k, v in _options.items() if v is defined %}
        {% if _query.append(k+'='+translate_uri_chars(v)) %}
        {% endif %}
    {% endfor %}
    {% if _query %}
        {% set _query = '&'.join(_query) %}
        "path": "/api/v1/token?{{ _query }}",
    {% else %}
        "path": "/api/v1/token/",
    {% endif %}
    "method": "GET"
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

# User source
# query
GET_USERSOURCE = """
{
    {% if path is defined %}
        "path": "{{ path }}",
    {% else %}
        {% if ver is defined %}
            {% set _ver = ver %}
        {% else %}
            {% set _ver = 'v1' %}
        {% endif %}
        {% if id is defined %}
            {% if customer_id is defined %}
                "path": "/api/{{ _ver }}/usersource/{{ id }}?customer_id={{ customer_id }}",
            {% else %}
                "path": "/api/{{ _ver }}/usersource/{{ id }}/",
            {% endif %}
        {% else %}
            {% set _options = {
                "customer_id": customer_id,
                "app_id": app_id,
                "realm_id": realm_id,
                "name": name
            } %}
            {% set _query = [] %}
            {% for k, v in _options.items() if v is defined %}
                {% if _query.append(k+'='+translate_uri_chars(v)) %}
                {% endif %}
            {% endfor %}
            {% if _query %}
                {% set _query = '&'.join(_query) %}
                "path": "/api/{{ _ver }}/usersource?{{ _query }}",
            {% else %}
                "path": "/api/{{ _ver }}/usersource/",
            {% endif %}
        {% endif %}
    {% endif %}
    "method": "GET"
}
"""

# add
ADD_USERSOURCE = """
{
    "path": "/api/v1/usersource/",
    "method": "POST",
    "body": {
        "customer_id": "{{ customer_id }}",
        "realm_id": "{{ realm_id }}",
        "type": {{ type }},
        {% set _usersource_params = {
            "prefix": prefix,
            "username_assertion": username_assertion,
            "favicon_url": favicon_url,
            "login_hint": login_hint,
        } %}
        {% for k, v in _usersource_params.items() if v is defined %}
            "{{ k }}": "{{ v }}",
        {% endfor %}
        {% if attr_mapping is defined and attr_mapping %}
            "attr_mapping": "{{ attr_mapping }}",
        {% endif %}
        {% if saml_params is defined %}
            {% set _saml_params = {
                "entity_id": entity_id,
                "login_url": login_url,
                "logout_url": logout_url,
                "signing_cert": signing_cert,
                "post_binding": post_binding,
                "include_subject": include_subject
            } %}
            "saml_params": {
                {% for k, v in _saml_params.items() if k in saml_params.keys() %}
                    "{{ k }}": "{{ saml_params[k] }}"{{ "," if not loop.last }}
                {% endfor %}
            },
        {% endif %}
        {% if oidc_params is defined %}
            {% set _oidc_params = {
                "issuer": issuer,
                "auth_uri": auth_uri,
                "token_uri": token_uri,
                "userinfo_uri": userinfo_uri,
                "logout_uri": logout_uri,
                "client_id": client_id,
                "client_secret": client_secret
            } %}
            "oidc_params": {
                {% for k, v in _oidc_params.items() if k in oidc_params.keys() %}
                    "{{ k }}": "{{ oidc_params[k] }}"{{ "," if not loop.last }}
                {% endfor %}
            },
        {% endif %}
        "name": "{{ name }}"
    }
}
"""

# delete
DELETE_USERSOURCE = """
{
    {% if customer_id is defined %}
        "path": "/api/v1/usersource/{{ id }}?customer_id={{ customer_id }}",
    {% else %}
        "path": "/api/v1/usersource/{{ id }}/",
    {% endif %}
    "method": "DELETE"
}
"""

# put
MODIFY_USERSOURCE = """
{
    "path": "/api/v1/usersource/{{ id }}/",
    "method": "PUT",
    "body": {
        {% if saml_params is defined %}
            {% set _saml_params = {
                "entity_id": entity_id,
                "login_url": login_url,
                "logout_url": logout_url,
                "signing_cert": signing_cert,
                "post_binding": post_binding,
                "include_subject": include_subject
            } %}
            "saml_params": {
                {% for k, v in _saml_params.items() if k in saml_params.keys() %}
                    "{{ k }}": "{{ saml_params[k] }}"{{ "," if not loop.last }}
                {% endfor %}
            },
        {% endif %}
        {% if oidc_params is defined %}
            {% set _oidc_params = {
                "issuer": issuer,
                "auth_uri": auth_uri,
                "token_uri": token_uri,
                "userinfo_uri": userinfo_uri,
                "logout_uri": logout_uri,
                "client_id": client_id,
                "client_secret": client_secret
            } %}
            "oidc_params": {
                {% for k, v in _oidc_params.items() if k in oidc_params.keys() %}
                    "{{ k }}": "{{ oidc_params[k] }}"{{ "," if not loop.last }}
                {% endfor %}
            },
        {% endif %}
        {% set _usersource_params = {
            "customer_id": customer_id,
            "name": name,
            "attr_mapping": attr_mapping,
            "username_assertion": username_assertion,
            "favicon_url": favicon_url,
            "login_hint": login_hint
        } %}
        {% for k, v in _usersource_params.items() if v is defined %}
            "{{ k }}": "{{ v }}"{{ "," if not loop.last }}
        {% endfor %}
    }
}
"""


# application
# query
GET_APPLICATION = """
{
    {% if path is defined %}
        "path": "{{ path }}",
    {% else %}
        {% if ver is defined %}
            {% set _ver = ver %}
        {% else %}
            {% set _ver = 'v1' %}
        {% endif %}
        {% if id is defined %}
            {% if customer_id is defined %}
                "path": "/api/{{ _ver }}/application/{{ id }}?customer_id={{ customer_id }}",
            {% else %}
                "path": "/api/{{ _ver }}/application/{{ id }}/",
            {% endif %}
        {% else %}
            {% set _options = {
                "customer_id": customer_id,
                "realm_id": realm_id,
                "name": name,
                "type": type,
                "prefix": prefix
            } %}
            {% set _query = [] %}
            {% for k, v in _options.items() if v is defined %}
                {% if _query.append(k+'='+translate_uri_chars(v)) %}
                {% endif %}
            {% endfor %}
            {% if _query %}
                {% set _query = '&'.join(_query) %}
                "path": "/api/{{ _ver }}/application?{{ _query }}",
            {% else %}
                "path": "/api/{{ _ver }}/application/",
            {% endif %}
        {% endif %}
    {% endif %}
    "method": "GET"
}
"""

# add
ADD_APPLICATION = """
{
    "path": "/api/v1/application/",
    "method": "POST",
    "body": {
        "customer_id": "{{ customer_id }}",
        "realm_id": "{{ realm_id }}",
        "type": {{ type }},
        {% set _application_params = {
            "prefix": prefix,
            "branding_id": branding_id,
            "profile_id": profile_id,
            "ttl": ttl,
            "access": access,
            "login_url": login_url,
            "logo_url": logo_url,
            "reverse_proxy_url": reverse_proxy_url
        } %}
        {% for k, v in _application_params.items() if v is defined %}
            "{{ k }}": "{{ v }}",
        {% endfor %}
        {% if attr_mapping is defined and attr_mapping %}
            "attr_mapping": "{{ attr_mapping }}",
        {% endif %}
        {% if saml_params is defined %}
            {% set _saml_params = {
                "entity_id": entity_id,
                "acs_url": acs_url,
                "slo_url": slo_url,
                "subject_nameid": subject_nameid,
                "signing_alg": signing_alg,
                "signing_cert_id": signing_cert_id,
                "sp_signing_cert": sp_signing_cert
            } %}
            "saml_params": {
                {% for k, v in _saml_params.items() if k in saml_params.keys() %}
                    "{{ k }}": "{{ saml_params[k] }}"{{ "," if not loop.last }}
                {% endfor %}
            },
        {% endif %}
        {% if oidc_params is defined %}
            {% set _oidc_params = {
                "audience_id": audience_id,
                "redirect_uris": redirect_uris,
                "signing_alg": signing_alg,
                "signing_cert_id": signing_cert_id
            } %}
            "oidc_params": {
                {% for k, v in _oidc_params.items() if k in oidc_params.keys() %}
                    "{{ k }}": "{{ oidc_params[k] }}"{{ "," if not loop.last }}
                {% endfor %}
            },
        {% endif %}
        "name": "{{ name }}"
    }
}
"""

# delete
DELETE_APPLICATION = """
{
    {% if customer_id is defined %}
        "path": "/api/v1/application/{{ id }}?customer_id={{ customer_id }}",
    {% else %}
        "path": "/api/v1/application/{{ id }}/",
    {% endif %}
    "method": "DELETE"
}
"""

# put
MODIFY_APPLICATION = """
{
    "path": "/api/v1/application/{{ id }}/",
    "method": "PUT",
    "body": {
        {% if saml_params is defined %}
            {% set _saml_params = {
                "entity_id": entity_id,
                "acs_url": acs_url,
                "slo_url": slo_url,
                "subject_nameid": subject_nameid,
                "signing_alg": signing_alg,
                "signing_cert_id": signing_cert_id,
                "sp_signing_cert": sp_signing_cert
            } %}
            "saml_params": {
                {% for k, v in _saml_params.items() if k in saml_params.keys() %}
                    "{{ k }}": "{{ saml_params[k] }}"{{ "," if not loop.last }}
                {% endfor %}
            },
        {% endif %}
        {% if oidc_params is defined %}
            {% set _oidc_params = {
                "audience_id": audience_id,
                "redirect_uris": redirect_uris,
                "signing_alg": signing_alg,
                "signing_cert_id": signing_cert_id
            } %}
            "oidc_params": {
                {% for k, v in _oidc_params.items() if k in oidc_params.keys() %}
                    "{{ k }}": "{{ oidc_params[k] }}"{{ "," if not loop.last }}
                {% endfor %}
            },
        {% endif %}
        {% set _application_params = {
            "name": name,
            "customer_id": customer_id,
            "attr_mapping": attr_mapping,
            "branding_id": branding_id,
            "profile_id": profile_id,
            "ttl": ttl,
            "access": access,
            "login_url": login_url,
            "logo_url": logo_url,
            "reverse_proxy_url": reverse_proxy_url
        } %}
        {% for k, v in _application_params.items() if v is defined %}
            "{{ k }}": "{{ v }}"{{ "," if not loop.last }}
        {% endfor %}
    }
}
"""

# associate an application with user sources
# query
GET_APPLICATION_USERSOURCE = """
{
    {% set _options = {
        "customer_id": customer_id,
        "user_source_id": user_source_id
    } %}
    {% set _query = [] %}
    {% for k, v in _options.items() if v is defined %}
        {% if _query.append(k+'='+translate_uri_chars(v)) %}
        {% endif %}
    {% endfor %}
    {% if _query %}
        {% set _query = '&'.join(_query) %}
        "path": "/api/v1/application/{{ app_id }}/user_source/?{{ _query }}",
    {% else %}
        "path": "/api/v1/application/{{ app_id }}/user_source",
    {% endif %}
    "method": "GET"
}
"""

# add
ADD_APPLICATION_USERSOURCE = """
{
    "path": "/api/v1/application/{{ app_id }}/user_source",
    "method": "POST",
    "body": {
        {% set _params = {
            "customer_id": customer_id,
            "user_source_id": user_source_id
        } %}
        {% for k, v in _params.items() if v is defined %}
            "{{ k }}": "{{ v }}"{{ "," if not loop.last }}
        {% endfor %}
    }
}
"""

# delete
DELETE_APPLICATION_USERSOURCE = """
{
    {% if customer_id is defined %}
        "path": "/api/v1/application/{{ app_id }}/user_source/{{ user_source_id }}?customer_id={{ customer_id }}",
    {% else %}
        "path": "/api/v1/application/{{ app_id }}/user_source/{{ user_source_id }}",
    {% endif %}
    "method": "DELETE"
}
"""

# put
MODIFY_APPLICATION_USERSOURCE = """
{
    "path": "/api/v1/application/{{ app_id }}/user_source",
    "method": "PUT",
    "body": {
        {% set _params = {
            "customer_id": customer_id,
            "user_source_ids": user_source_ids,
            "default_usersource_id": default_usersource_id
        } %}
        {% for k, v in _params.items() if v is defined %}
            "{{ k }}": "{{ v }}"{{ "," if not loop.last }}
        {% endfor %}
    }
}
"""

# signing cert
# query
GET_CERTIFICATE = """
{
    {% if id is defined %}
        {% if customer_id is defined %}
            "path": "/api/v1/certificate/{{ id }}?customer_id={{ customer_id }}",
        {% else %}
            "path": "/api/v1/certificate/{{ id }}/",
        {% endif %}
    {% else %}
        {% set _options = {
            "customer_id": customer_id,
            "name": name,
            "app_id": app_id,
        } %}
        {% set _query = [] %}
        {% for k, v in _options.items() if v is defined %}
            {% if _query.append(k+'='+translate_uri_chars(v)) %}
            {% endif %}
        {% endfor %}
        {% if _query %}
            {% set _query = '&'.join(_query) %}
            "path": "/api/v1/certificate?{{ _query }}",
        {% endif %}
    {% endif %}
    "method": "GET"
}
"""

# add
ADD_CERTIFICATE = """
{
    "path": "/api/v1/certificate/",
    "method": "POST",
    "body": {
        {% set _options = {
            "customer_id": customer_id,
            "certificate": certificate,
            "private_key": private_key
        } %}
        {% for k, v in _options.items() if v is defined %}
            "{{ k }}": {{ v }},
        {% endfor %}
        "name": "{{ name }}"
    }
}
"""

# delete
DELETE_CERTIFICATE = """
{
    {% if customer_id is defined %}
        "path": "/api/v1/certificate/{{ id }}/?customer_id={{ customer_id }}",
    {% else %}
        "path": "/api/v1/certificate/{{ id }}/",
    {% endif %}
    "method": "DELETE"
}
"""

# put
MODIFY_CERTIFICATE = """
{
    "path": "/api/v1/certificate/{{ id }}/",
    "method": "PUT",
    "body": {
        {% set _options = {
            "customer_id": customer_id,
            "name": name
        } %}
        {% for k, v in _options.items() if v is defined %}
            "{{ k }}": "{{ v }}"{{ "," if not loop.last }}
        {% endfor %}
    }
}
"""
