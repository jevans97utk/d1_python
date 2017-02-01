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
"""This module implements GMNTestClient, which extends
d1_client.mnclient.MemberNodeClient with GMN specific test functionality. The
REST interfaces on GMN that provide this functionality are prefixed with
"/diag/" and are only enabled when GMN runs in debug mode. The interfaces are
not versioned, and so there is no version tag (such as "v1") in the URL for
these methods.
"""

# Stdlib.
import glob
import json
import logging
import os
import re

# D1
import d1_client.mnclient
import d1_common.types.dataoneTypes
import d1_common.types.exceptions

# Constants.
GMN_TEST_SUBJECT_PUBLIC = 'public'
GMN_TEST_SUBJECT_TRUSTED = 'gmn_test_subject_trusted'


class GMNTestClient(d1_client.mnclient.MemberNodeClient):
  def __init__(self, *args, **kwargs):
    """Extend MemberNodeClient with GMN specific diagnostics wrappers.
    See d1baseclient.DataONEBaseClient for args.
    """
    self.logger = logging.getLogger(__file__)
    d1_client.mnclient.MemberNodeClient.__init__(self, *args, **kwargs)

  def _get_api_version_path_element(self):
    """Override the default API version selection to use GMNs custom /diag/
    endpoint."""
    return 'diag'

  def gmn_vse_provide_subject(self, subject):
    """GMN Vendor Specific Extension: Simulate subject."""
    return {'VENDOR_INCLUDE_SUBJECTS': subject}

  def gmn_vse_enable_sql_profiling(self):
    """GMN Vendor Specific Extension: Enable SQL profiling."""
    return {'VENDOR_PROFILE_SQL': 1}

  def gmn_vse_enable_python_profiling(self):
    """GMN Vendor Specific Extension: Enable Python profiling."""
    return {'VENDOR_PROFILE_PYTHON': 1}

  def get_resource_path(self, path):
    """Get path to test resources."""
    resource_path = os.path.abspath(
      os.path.join(
        os.path.dirname(__file__), '../../../../resources/')
    )
    return os.path.join(resource_path, path)

  # ----------------------------------------------------------------------------
  # Replication.
  # ----------------------------------------------------------------------------

  def get_replication_queue(self, headers=None):
    response = self.GET('get_replication_queue', headers=headers)
    return response.content

  def clear_replication_queue(self, headers=None):
    response = self.GET('clear_replication_queue', headers=headers)
    return self._read_boolean_response(response)

  def create_replication_queue(self, pid, sysmeta_pyxb, sourceNode, vendorSpecific=None):
    mmp_fields = {
      'pid': pid.encode('utf-8'),
      'sourceNode': sourceNode,
      'sysmeta': ('sysmeta.xml', sysmeta_pyxb.toxml().encode('utf-8')),
    }
    response = self.POST(
      ['replicate', pid],
      fields=mmp_fields,
      headers=vendorSpecific
    )
    return self._read_boolean_response(response)

  # ----------------------------------------------------------------------------
  # Access Policy.
  # ----------------------------------------------------------------------------

  def set_access_policy(self, pid, access_policy, headers=None):
    mmp_fields = {
      'access_policy': ('access_policy', access_policy.toxml().encode('utf-8')),
    }
    return self.POST(['set_access_policy', pid], fields=mmp_fields, headers=headers)

  def delete_all_access_policies(self, headers=None):
    response = self.GET('delete_all_access_policies', headers=headers)
    return self._read_boolean_response(response)

  def get_access_policy(self, pid, headers=None):
    response = self.GET(['get_access_policy', pid], headers=headers)
    return response.content

  # ----------------------------------------------------------------------------
  # Authentication.
  # ----------------------------------------------------------------------------

  def echo_session(self, headers=None):
    response = self.GET('echo_session', headers=headers)
    return response.content

  
  def whitelist_subject(self, subject_str, headers=None):
    """Add a subject to the whitelist"""
    mmp_fields = {
      'subject': subject_str,
    }
    response = self.POST('whitelist_subject', fields=mmp_fields, headers=headers)
    return response.content

  # ----------------------------------------------------------------------------
  # Misc.
  # ----------------------------------------------------------------------------

  def create(self, pid, obj, sysmeta_pyxb, vendorSpecific=None):
    if vendorSpecific is None:
      vendorSpecific = {}
    mmp_fields = {
      'pid': pid.encode('utf-8'),
      'object': ('content.bin', obj),
      'sysmeta': ('sysmeta.xml', sysmeta_pyxb.toxml().encode('utf-8')),
    }
    response = self.POST(
      ['create', pid],
      fields=mmp_fields,
      headers=vendorSpecific
    )
    return self._read_boolean_response(response)

  def slash(self, arg1, arg2, arg3, headers=None):
    response = self.GET(['slash', arg1, arg2, arg3], headers=headers)
    return response.content

  def exception(self, exception_type):
    response = self.GET(['exception', exception_type], headers=headers)
    return response.content

  def echo_request_object(self, headers=None):
    response = self.GET('echo_request_object', headers=headers)
    return response.content

  def echo_raw_post_data(self, headers=None):
    response = self.GET('echo_raw_post_data', headers=headers)
    return response.content

  def delete_all_objects(self, headers=None):
    response = self.GET('delete_all_objects', headers=headers)
    return self._read_boolean_response(response)

  def test_delete_single_object(self, pid, headers=None):
    response = self.GET(['delete_single_object', pid], headers=headers)
    return self._read_boolean_response(response)

  def get_setting(self, setting, headers=None):
    response = self.GET(['get_setting', setting], headers=headers)
    return response.json()

  # ----------------------------------------------------------------------------
  # Event Log.
  # ----------------------------------------------------------------------------

  def delete_event_log(self, headers=None):
    """Delete event log for all objects.
    """
    response = self.GET('delete_event_log', headers=headers)
    return self._read_boolean_response(response)

  def inject_fictional_event_log(self, event_log_csv, headers=None):
    """Inject a fake event log.
    """
    mmp_fields = {
      'csv': ('csv', event_log_csv),
    }
    response = self.POST('inject_fictional_event_log', fields=mmp_fields, headers=headers)
    return self._read_boolean_response(response)

  # ----------------------------------------------------------------------------
  # Concurrency.
  # ----------------------------------------------------------------------------

  def concurrency_clear(self, headers=None):
    """Clear test key/vals.
    """
    return self.GET('concurrency_clear', headers=headers)

  def concurrency_read_lock(self, key, sleep_before, sleep_after, headers=None):
    """Test PID read locking.
    """
    return self.GET(['concurrency_read_lock', key, sleep_before, sleep_after], headers=headers)

  def concurrency_write_lock(self, key, val, sleep_before, sleep_after, headers=None):
    """Test PID write locking.
    """
    return self.GET(['concurrency_write_lock', key, val, sleep_before, sleep_after], headers=headers)

  def concurrency_get_dictionary_id(self, headers=None):
    """Get dictionary ID.
    """
    return self.GET('concurrency_get_dictionary_id', headers=headers)

# ==============================================================================


def include_subjects(subjects):
  if isinstance(subjects, basestring):
    subjects = [subjects]
  return {'VENDOR_INCLUDE_SUBJECTS': '\t'.join(subjects)}


def populate_mn(client, filedir):
  for sysmeta_path in sorted(glob.glob(os.path.join(filedir, '*.sysmeta'))):
    # Get name of corresponding object and open it.
    object_path = re.match(r'(.*)\.sysmeta', sysmeta_path).group(1)
    object_file = open(object_path, 'r')

    # The pid is stored in the sysmeta.
    sysmeta_file = open(sysmeta_path, 'r')
    sysmeta_xml = sysmeta_file.read()
    sysmeta_pyxb = d1_common.types.dataoneTypes.CreateFromDocument(sysmeta_xml)
    sysmeta_pyxb.rightsHolder = 'test_user_1'

    headers = include_subjects('test_user_1')
    headers.update({'VENDOR_TEST_OBJECT': 1})

    client.create(
      sysmeta_pyxb.identifier.value(),
      object_file,
      sysmeta_pyxb,
      vendorSpecific=headers
    )


def rest_call(self, func, python_profile=False, sql_profile=False, *args, **kwargs):
  """Wrap a rest call up with automatic handling of vendor specific extensions
  for profiling and selecting subject."""
  vendor_specific = {}
  # When not using certificates, the subject is passed in via a vendor
  # specific extension that is supported by all the REST calls in GMN.
  if not settings.USE_CERTS:
    vendor_specific.update(test_utilities.gmn_vse_provide_subject(self.subject))
  # Enable python profiling if requested.
  if python_profile:
    vendor_specific.update(test_utilities.gmn_vse_enable_python_profiling())
  if sql_profile:
    vendor_specific.update(test_utilities.gmn_vse_enable_sql_profiling())
  return func(vendorSpecific=vendor_specific, *args, **kwargs)
