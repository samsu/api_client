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


# customer account
# query customer account
GET_ACCOUNT = """
{
    "path": "/FortiGlobalDev/FortinetOneIdentityService.asmx/Process",
    "method": "POST",
    "body": {
        "d": {
            "__type" : "FortinetOneAPI.IdentityService.GetAccountDetailsRequest", 
            "__version" : "1",
            "request_channel" : "FTC",
            {% set _options = {
                "account_id": id,
                "account_email": email,
                "serial_number": sn,
                "user_id": user_id
            } %}
            "search_filters" :
            {
            {% for k, v in _options.iteritems() if v is defined %}
              {{ k }}: "{{ v }}"{{ "," if not loop.last }}
            {% endfor %}
            } 
        }
    }
}
"""

GET_APPLIST = """
{
    "path": "/FortiGlobalDev/FortinetOneCommonService.asmx/Process",
    "method": "POST",
    "body": {
        "d": {
            "__type": "FortinetOneAPI.CommonService.GetPortalListRequest",
            {% if version is defined %}
                "__version": "{{ version }}",
            {% else %}
                "__version": "1",
            {% endif %}
            "request_channel": "CustomerManagement"
        }
    }
}
"""

GET_ACCOUNTLIST = """
{
    "path": "/FortiGlobalDev/FortinetOneIdentityService.asmx/Process",
    "method": "POST",
    "body": {
        "d": {
            "__type" : "FortinetOneAPI.IdentityService.GetLoginAccountsByEmailRequest",
            {% if version is defined %}
                "__version": "{{ version }}",
            {% else %}
                "__version": "1",
            {% endif %}
            "search_filters": {
                "email": "{{ fortinet_id }}"
            },
            {% if service_type is defined %}
                "request_channel": "{{ service_type }}"
            {% else %}
                "request_channel": "FTC"
            {% endif %}
        }
    }
}
"""

# Get user balance
GET_BALANCE = """
{
    "path": "/FortiGlobalDev/FortiAuthService.asmx/Process",
    "method": "POST",
    "body": {
        "d": {
            "__type" : "FortiGlobal.FASInquiryRequest",
            {% if version is defined %}
                "__version": "{{ version }}",
            {% else %}
                "__version": "1",
            {% endif %}
            {% if sw_version is defined %}
                "__SW_version": "{{ sw_version }}",
            {% else %}
                "__SW_version": "xxxx",
            {% endif %}
            {% if sw_build is defined %}
                "__SW_build": "{{ sw_build }}",
            {% else %}
                "__SW_build": "yyyyy",
            {% endif %}
            "user_id": "{{ id }}"
        }
    }
}
"""


# User balance update
POST_USAGE = """
{
    "path": "/FortiGlobalDev/FortiAuthService.asmx/Process",
    "method": "POST",
    "body": {
        "d": {
            "__type": "FortiGlobal.FASBalanceUpdateRequest",
            {% if version is defined %}
                "__version": "{{ version }}",
            {% else %}
                "__version": "1",
            {% endif %}
            {% if sw_version is defined %}
                "__SW_version": "{{ sw_version }}",
            {% else %}
                "__SW_version": "xxxx",
            {% endif %}
            {% if sw_build is defined %}
                "__SW_build": "{{ sw_build }}",
            {% else %}
                "__SW_build": "yyyyy",
            {% endif %}
            "Used_Points":
            [
                {
                    "User_ID": "{{ user_id }}",
                    "External_Id": "{{ ext_id }}",
                    "Name_Space": "{{ ns }}",
                    "Start_Date": "{{ start_date }}",
                    "End_Date": "{{ end_date }}",
                    "Parameter_Type": "FAS_Number_Of_User_Months",
                    "Parameter_Value": "{{ usage }}"
                }
            ]
        }
    }
}
"""
