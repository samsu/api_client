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
            {% for k, v in _options.items() if v is defined %}
              "{{ k }}": "{{ v }}"{{ "," if not loop.last }}
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

# Get all users' balance
GET_BATCH_BALANCE = """
{
    "path": "/CloudAPI/V3/FortiTokenCloud/FortiTokenCloudService.asmx/GetPointBalanceForAllUsers",
    "method": "POST",
    "body": {
        "d": {
            "__type": "FortinetOne.API.V3.FortiTokenCloud.GetPointBalanceForAllUsersPayload",
            {% if page_index is defined %}
                "page_index": "{{ page_index }}",
            {% else %}
                "page_index": "1",
            {% endif %}
            {% if page_size is defined %}
                "page_size": "{{ page_size }}"
            {% else %}
                "page_size": "1000"
            {% endif %}
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

# On-premises agent(OPA) license
ADD_OPA_LICENSE = """
{
    "path": "/CloudAPI_IAM/V3/FortiTokenCloud/FortiTokenCloudService.asmx/GetNewFACVMLicense",
    "method": "POST",
    "body": {
        "d": {
            "__type": "FortinetOne.API.V3.FortiTokenCloud.GetNewFACVMLicensePayload",
            "license_version": "latest"
        }
    }
}
"""

# query OPA license
GET_OPA_LICENSE = """
{
    "path": "/CloudAPI_IAM/V3/FortiTokenCloud/FortiTokenCloudService.asmx/GetExistingFACVMLicense",
    "method": "POST",
    "body": {
        "d": {
            "__type": "FortinetOne.API.V3.FortiTokenCloud.GetExistingFACVMLicensePayload",
            "serial_number": "{{ sn }}",
            "license_version": "latest"
        }
    }
}
"""

GET_FTC_LICENSE = """
{
    "path": "/CloudAPI/V3/FortiTokenCloud/FortiTokenCloudService.asmx/GetProductEntitlements",
    "method": "POST",
    "body": {
        "d": {
            "__type": "FortinetOne.API.V3.FortiTokenCloud.GetProductEntitlementsPayload",
            "accountIds": ["{{ id }}"]
        }
    }
}
"""

GET_BATCH_FTC_LICENSE = """
{
    "path": "/CloudAPI/V3/FortiTokenCloud/FortiTokenCloudService.asmx/GetProductEntitlementsForAllAccounts",
    "method": "POST",
    "body": {
        "d": {
            "__type": "FortinetOne.API.V3.FortiTokenCloud.GetProductEntitlementsForAllAccountsPayload",
            {% if page_index is defined %}
                "page_index": "{{ page_index }}",
            {% else %}
                "page_index": "1",
            {% endif %}
            {% if page_size is defined %}
                "page_size": "{{ page_size }}"
            {% else %}
                "page_size": "1000"
            {% endif %}
        }
    }
}
"""


GET_LICENSE = """
{
    "path": "/FortiGlobal/FortinetOneProductService.asmx/Process",
    "method": "POST",
    "body": {
        "d": {
            "__type": "FortinetOneAPI.ProductService.GetLicenseDetailsRequest",
            "__version": "2.0",
            "request_channel": "FTC",
            {% set _options = {
                "account_id": id,
                "license_number": license_number,
                "serial_number": serial_number
            } %}
            "search_filters":
            {
            {% for k, v in _options.items() if v is defined %}
              "{{ k }}": "{{ v }}"{{ "," if not loop.last }}
            {% endfor %}
            }
        }
    }
}
"""


GET_MIGRATION_TAG = """
{
    "path": "/CloudAPI/V3/FortiTokenCloud/FortiTokenCloudService.asmx/GetFTMMigrationTag",
    "method": "POST",
    "body": {
        "d": {
            "__type": "FortinetOne.API.V3.FortiTokenCloud.GetFTMMigrationTagPayload",
            "accountId": "{{ id }}"
        }
    }
}
"""


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


GET_DEVICE_LIST = """
{
    "path": "/CloudAPI/V3/Common/FortinetOneProductService.asmx/GetProductList",
    "method": "POST",
    "body": {
        "d": {
            "__type": "FortinetOne.API.V3.Common.GetProductListPayload",
            "account_id": "{{ id }}"
        }
    }
}
"""
