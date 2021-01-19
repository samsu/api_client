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

from . import fas

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

#REALM
# query

GET_REALM = fas.GET_REALM

# User
# query
GET_USER = fas.GET_USER

# Add Users

ADD_USER = fas.ADD_USER

# put
MODIFY_USER = fas.MODIFY_USER

# delete
DELETE_USER = fas.DELETE_USER

# authentication
ADD_AUTH = fas.ADD_AUTH

GET_AUTH = fas.GET_AUTH

# Version
GET_VERSION = fas.GET_VERSION

