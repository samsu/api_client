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

# LOGIN

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

# Add Users

ADD_USER = """
{
    "path": "/api/v1/user",
    "method": "POST",
    "body": {
        {% if realm is defined %}
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
        {% if user_data is defined %}
            "user_data": "{{ user_data }}",
        {% endif %}
        "username": "{{ username }}",
        "email": "{{ email }}"
    }
}
"""

# Balance

GET_BALANCE = """
{
    "path": "/api/v1/balance",
    "method": "GET"
}
"""

# Version
GET_VERSION = """
{
    "path": "/version/",
    "method": "GET"
}
"""
