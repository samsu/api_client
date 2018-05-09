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

# login
LOGIN = """
{
    {% if next_url is defined %} 
        "path": "/RegistrationDev/Main.aspx?from=FAS&RedirectURL={{ next_url }}",
    {% else %}
        "path": "/RegistrationDev/Main.aspx?from=FAS&RedirectURL=",
    {% endif %}
    "method": "POST",
    "body": {
        "d": {
            "User_ID": "395939",
            "__SW_version": "xxxx",
            "__SW_build": "yyyyy",
            "__type": "FortiGlobal.FortiCASBAccountInfoRequest",
            "__version": "1"
        }
    }
}
"""

# customer account
# query customer account
GET_ACCOUNT = """
{
    "path": "/FortiGlobalDev/FortiAuthService.asmx/Process",    
    "method": "POST",
    "body": {    
        "d": {
            "__type": "FortiGlobal.FASAccountInfoRequest",
            {% if id is defined %}
                "user_id": "{{ id }}",
            {% endif %}
            {% if sn is defined %}
                "serial_number": "{{ sn }}",
            {% endif %}
            {% if email is defined %}
                "User_Email": "{{ email }}",
            {% endif %}
            {% if account_id is defined %}
                "account_id": "{{ account_id }}",
            {% endif %}
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
                "__SW_build": "{{ sw_build }}"
            {% else %}
                "__SW_build": "yyyyy"
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
