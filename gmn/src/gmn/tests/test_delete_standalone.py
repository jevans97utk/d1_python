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
"""Test MNStorage.delete() for "standalone" objects

These are single objects that are not members of a revision chain (both
obsoletes and obsoletedBy are unset). For v2, the objects may or may not have a
SID
"""
from __future__ import absolute_import

import responses

import d1_common.xml
import d1_common.util
import d1_common.types.exceptions

import gmn.tests.gmn_mock
import gmn.tests.gmn_test_case


class TestDeleteStandalone(gmn.tests.gmn_test_case.D1TestCase):
  @responses.activate
  @gmn.tests.gmn_mock.disable_auth_decorator
  def _assert_delete(self, client, binding, sid=None):
    pid, sid, send_sciobj_str, send_sysmeta_pyxb = (
      self.create_obj(client, binding, sid=sid)
    )
    # Is retrievable
    recv_sciobj_str, recv_sysmeta_pyxb = self.get_obj(client, pid)
    self.assert_sysmeta_pid_and_sid(recv_sysmeta_pyxb, pid, sid)
    # Delete
    identifier_pyxb = client.delete(pid)
    self.assertEqual(identifier_pyxb.value(), pid)
    # Is no longer retrievable so new delete() raises 404
    with self.assertRaises(d1_common.types.exceptions.NotFound):
      client.delete(pid)
    # PID can now be reused
    self.create_obj(client, binding, pid, sid)
    # Is again retrievable
    reused_sysmeta_pyxb = self.client_v2.getSystemMetadata(pid)
    self.assert_sysmeta_pid_and_sid(reused_sysmeta_pyxb, pid, sid)

  def test_0010(self):
    """MNStorage.delete(): Standalone object, SID unsupported in v1"""
    self._assert_delete(self.client_v1, self.v1)

  def test_0020(self):
    """MNStorage.delete(): Standalone object without SID"""
    self._assert_delete(self.client_v2, self.v2)

  def test_0030(self):
    """MNStorage.delete(): Standalone object with SID"""
    self._assert_delete(self.client_v2, self.v2, sid=True)