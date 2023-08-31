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

#    FortiCare API request format templates.

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
    "path": "/FortiGlobal/FortiAuthService.asmx/Process",
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
    "path": "/FortiGlobal/FortiAuthService.asmx/Process",
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
    "path": "/FortiGlobal/FortiAuthService.asmx/Process",
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

GET_APPLIST = """
{
    "path": "/FortiGlobal/FortiCareService.asmx/Process",
    "method": "POST",
    "body": {
        "d": {
            "__type": "FortiGlobal.FortinetAppListRequest",
            {% if version is defined %}
                "__version": "{{ version }}",
            {% else %}
                "__version": "1",
            {% endif %}
            "request_app": "CustomerManagement"
        }
    }
}
"""

GET_PROD_APPLIST = GET_APPLIST

GET_ACCOUNTLIST = """
{
    "path": "/FortiGlobal/FortiCareService.asmx/Process",
    "method": "POST",
    "body": {
                "d": {
                      "__type" : "FortiGlobal.AccountSelectionRequest",
                      {% if version is defined %}
                      "__version": "{{ version }}",
                      {% else %}
                      "__version": "1",
                      {% endif %}
                      "fortinet_id": "{{ fortinet_id }}",
                      {% if service_type is defined %}
                      "service_type": "{{ service_type }}"
                      {% else %}
                      "service_type": "FAS"
                      {% endif %}
                }
    }
}
"""

GET_PROD_ACCOUNTLIST = GET_ACCOUNTLIST


GET_SMS_LICENSE = """
{
    "path": "/CloudAPI/V3/FortiTokenCloud/FortiTokenCloudService.asmx/GetSMSBalance",
    "method": "POST",
    "body": {
        "d": {
            "__type": "FortinetOne.API.V3.FortiTokenCloud.GetSMSBalancePayload",
            "account_id": "{{ id }}"
        }
    }
}
"""


GET_BATCH_SMS_LICENSE = """
{
    "path": "/CloudAPI/V3/FortiTokenCloud/FortiTokenCloudService.asmx/GetSMSBalanceForAllAccounts",
    "method": "POST",
    "body": {
        "d": {
            "__type": "FortinetOne.API.V3.FortiTokenCloud.GetSMSBalanceForAllAccountsPayload"
        }
    }
}
"""


POST_SMS_USAGE = """
{
    "path": "/CloudAPI/V3/FortiTokenCloud/FortiTokenCloudService.asmx/UpdateSMSUsage",
    "method": "POST",
    "body": {
        "d": {
            "__type": "FortinetOne.API.V3.FortiTokenCloud.UpdateSMSUsagePayload",
            {% if name_space is defined %}
                "name_space": "{{ name_space }}",
            {% else %}
                "name_space": "",
            {% endif %}
            "account_id": "{{ account_id }}",
            "serial_number": "{{ serial_number }}",
            "unique_id": "{{ unique_id }}",
            "start_date": "{{ start_date }}",
            "end_date": "{{ end_date }}",
            "used_points": "{{ used_points }}"
        }
    }
}
"""


GET_FORTITRUST_LICENSE = """
{
    "path": "/CloudAPI/V3/FortiTrust/FortiTrustService.asmx/GetProductEntitlements",
    "method": "POST",
    "body": {
        "d": {
            "__type": "FortinetOne.API.V3.FortiTrust.GetProductEntitlementsPayload",
            "account_id": "{{ id }}"
        }
    }
}
"""


GET_BATCH_FORTITRUST_LICENSE = """
{
    "path": "/CloudAPI/V3/FortiTrust/FortiTrustService.asmx/GetProductEntitlementsForAllAccounts",
    "method": "POST",
    "body": {
        "d": {
            "__type": "FortinetOne.API.V3.FortiTrust.GetProductEntitlementsForAllAccountsPayload"
        }
    }
}
"""
