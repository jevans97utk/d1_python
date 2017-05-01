# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2016 DataONE
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

import d1_client.mnclient_2_0

import d1_common.const
import d1_common.date_time
import d1_common.types.dataoneTypes_v1
import d1_common.types.dataoneTypes_v2_0
import d1_common.types.exceptions
import d1_common.util

import d1_test.mock_api.get_log_records as mock_log_records
import d1_test.mock_api.tests.settings as settings

import responses


class TestMockLogRecords(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    d1_common.util.log_setup(is_debug=True)

  def setUp(self):
    self.client = d1_client.mnclient_2_0.MemberNodeClient_2_0(
      base_url=settings.MN_RESPONSES_BASE_URL
    )

  @responses.activate
  def test_0010(self):
    """mock_api.getLogRecords() returns a DataONE Log PyXB object"""
    mock_log_records.add_callback(settings.MN_RESPONSES_BASE_URL)
    self.assertIsInstance(
      self.client.getLogRecords(),
      d1_common.types.dataoneTypes_v2_0.Log,
    )

  @responses.activate
  def test_0020(self):
    """mock_api.getLogRecords(): Passing a trigger header triggers a DataONEException"""
    mock_log_records.add_callback(settings.MN_RESPONSES_BASE_URL)
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self.client.getLogRecords,
      'test_pid', vendorSpecific={'trigger': '404'}
    )
