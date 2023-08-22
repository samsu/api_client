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
    {% if sender is defined %}
        "path": "/version?sender={{ sender }}",
    {% else %}
        "path": "/version/",
    {% endif %}
    "method": "GET"
}
"""

# Notification
# add
ADD_NOTIFICATION = """
{
    "path": "/v1/notification",
    "method": "POST",
    "body": {
        {% set _options = {
            "sender": sender,
            "platform": platform,
            "app": app,
            "registration_id": registration_id,
            "email": email,
            "mobile_number": mobile_number
        } %}

        {% for k, v in _options.items() if v is defined %}
            "{{ k }}": "{{ v }}",
        {% endfor %}
        "message": {{ message }}
    }
}
"""
