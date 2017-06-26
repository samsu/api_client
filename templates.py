# Copyright (c) 2015 Fortinet, Inc.
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

#    FortiOS API request format templates.

# About api request message naming regulations:
# Prefix         HTTP method
# ADD_XXX    -->    POST
# SET_XXX    -->    PUT
# DELETE_XXX -->    DELETE
# GET_XXX    -->    GET


## usergroups
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
CREATE_USERGROUPS = """
{
    "path": "/api/v1/usergroups/",
    "method": "POST",
    "body": {
        "name": "{{ name }}"
    }
}
"""

# delete an usergroup
DELETE_USERGROUPS = """
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
        {% if name is defined %}
            "path": "/api/v1/localusers/?name={{ name }}",
        {% else %}
            "path": "/api/v1/localusers/",
        {% endif %}
    {% endif %}
    "method": "GET"
}
"""

# create an usergroup
CREATE_USERS = """
{
    "path": "/api/v1/localusers/",
    "method": "POST",
    "body": {
        "name": "{{ name }}"
    }
}
"""

# delete an usergroup
DELETE_USERS = """
{
    "path": "/api/v1/localusers/",
    "method": "DELETE",
    "body": {
        "name": "{{ name }}"
    }
}
"""
