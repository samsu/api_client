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

#    SCIM API request format templates for job.py sync operations

# About api request message naming regulations:
# Prefix         HTTP method
# GET_XXX      -->    GET
# CREATE_XXX   -->    POST
# UPDATE_XXX   -->    PUT
# DELETE_XXX   -->    DELETE
# PATCH_XXX    -->    PATCH

# Connection testing
TEST_USER_CONNECTION = """
{
    "path": "{{ base_path | default('') }}/Users/{{ test_user }}",
    "method": "GET"
}
"""
