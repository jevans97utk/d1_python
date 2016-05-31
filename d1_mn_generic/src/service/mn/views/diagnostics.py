#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2012 DataONE
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

''':mod:`views.diagnostics`
===========================

:Synopsis:
  REST call handlers for GMN diagnostic APIs.
  These are used in various diagnostics, debugging and testing scenarios.
  Access is unrestricted in debug mode. Disabled in production.
:Author: DataONE (Dahl)
'''
# Stdlib.
import cgi
import csv
import os
import pprint
import time
import urlparse

# Django.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.db.models import Q
from django.conf import settings

# D1.
import d1_common.const
import d1_common.date_time
import d1_common.types.exceptions
import d1_common.types.generated.dataoneTypes as dataoneTypes

# App.
import service.view_asserts
import service.auth
import service.db_filter
import service.event_log
import service.models
import service.node_registry
import service.psycopg_adapter
import service.restrict_to_verb
import service.sysmeta_store
import service.urls
import service.util
import service.view_shared

# ------------------------------------------------------------------------------
# Diagnostics portal.
# ------------------------------------------------------------------------------

@service.restrict_to_verb.get
def diagnostics(request):
  if 'clear_db' in request.GET:
    _delete_all_objects()
    _clear_replication_queue()
    _delete_subjects_and_permissions()
  if request.path.endswith('/'):
    return HttpResponseRedirect(request.path[:-1])
  return render_to_response('diag.html', d1_common.const.CONTENT_TYPE_XHTML)

# ------------------------------------------------------------------------------
# Replication.
# ------------------------------------------------------------------------------

@service.restrict_to_verb.get
def get_replication_queue(request):
  q = service.models.ReplicationQueue.objects.all()
  if 'excludecompleted' in request.GET:
    q = service.models.ReplicationQueue.objects.filter(
      ~Q(status__status='completed'))
  return render_to_response('replicate_get_queue.xml',
    {'replication_queue': q },
    content_type=d1_common.const.CONTENT_TYPE_XML)


@service.restrict_to_verb.get
def clear_replication_queue(request):
  _clear_replication_queue()
  return service.view_shared.http_response_with_boolean_true_type()


def _clear_replication_queue():
  service.models.ReplicationQueue.objects.all().delete()


# ------------------------------------------------------------------------------
# Access Policy.
# ------------------------------------------------------------------------------

@service.restrict_to_verb.get
def set_access_policy(request, pid):
  service.view_asserts.object_exists(pid)
  service.view_asserts.post_has_mime_parts(request, (('file', 'access_policy'),))
  access_policy_xml = request.FILES['access_policy'].read()
  access_policy = dataoneTypes.CreateFromDocument(access_policy_xml)
  service.auth.set_access_policy(pid, access_policy)
  return service.view_shared.http_response_with_boolean_true_type()


@service.restrict_to_verb.get
def delete_all_access_policies(request):
  # The deletes are cascaded so all subjects are also deleted.
  service.models.Permission.objects.all().delete()
  return service.view_shared.http_response_with_boolean_true_type()

# ------------------------------------------------------------------------------
# Authentication.
# ------------------------------------------------------------------------------

@service.restrict_to_verb.get
def echo_session(request):
  return render_to_response('echo_session.xhtml',
                            {'subjects': sorted(request.subjects) },
                            content_type=d1_common.const.CONTENT_TYPE_XHTML)


@service.restrict_to_verb.get
def trusted_subjects(request):
  return render_to_response('trusted_subjects.xhtml',
    {'subjects': sorted(service.node_registry.get_cn_subjects() |
                        settings.DATAONE_TRUSTED_SUBJECTS) },
    content_type=d1_common.const.CONTENT_TYPE_XHTML)

# ------------------------------------------------------------------------------
# Misc.
# ------------------------------------------------------------------------------

def create(request, pid):
  '''Version of create() that performs no locking, testing or validation.
  Used for inserting test objects.'''
  sysmeta_xml = request.FILES['sysmeta'].read().decode('utf-8')
  sysmeta = service.view_shared.deserialize_system_metadata(sysmeta_xml)
  service.view_shared.create(request, pid, sysmeta)
  return service.view_shared.http_response_with_boolean_true_type()


@service.restrict_to_verb.get
def slash(request, p1, p2, p3):
  '''Test that GMN correctly handles three arguments separated by slashes'''
  return render_to_response('test_slash.html', {'p1': p1, 'p2': p2, 'p3': p3})


@service.restrict_to_verb.get
def exception(request, exception_type):
  '''Test that GMN correctly catches and serializes exceptions raised by views'''
  if exception_type == 'python':
    raise Exception("Test Python Exception")
  elif exception_type == 'dataone':
    raise d1_common.types.exceptions.InvalidRequest(0, 'Test DataONE Exception')

  return service.view_shared.http_response_with_boolean_true_type()


@service.restrict_to_verb.get
def echo_request_object(request):
  pp = pprint.PrettyPrinter(indent=2)
  return HttpResponse('<pre>{0}</pre>'.format(cgi.escape(pp.pformat(request))))


@service.restrict_to_verb.get
def permissions_for_object(request, pid):
  service.view_asserts.object_exists(pid)
  subjects = []
  permissions = service.models.Permission.objects.filter(object__pid = pid)
  for permission in permissions:
    action = service.auth.level_action_map[permission.level]
    subjects.append((permission.subject.subject , action))
  return render_to_response('permissions_for_object.xhtml', locals(),
                          content_type=d1_common.const.CONTENT_TYPE_XHTML)

@service.restrict_to_verb.get
def get_setting(request, setting):
  '''Get a value from settings.py or settings_site.py'''
  return HttpResponse(getattr(settings, setting, '<UNKNOWN SETTING>'),
                      d1_common.const.CONTENT_TYPE_TEXT)

#@service.restrict_to_verb.post
def echo_raw_post_data(request):
  return HttpResponse(request.raw_post_data)


@service.restrict_to_verb.get
def delete_all_objects(request):
  _delete_all_objects()
  delete_event_log(request)
  return service.view_shared.http_response_with_boolean_true_type()


def _delete_all_objects():
  for object_ in service.models.ScienceObject.objects.all():
    _delete_object(object_.pid)


def _delete_subjects_and_permissions():
  service.models.Permission.objects.all().delete()
  service.models.PermissionSubject.objects.all().delete()


@service.restrict_to_verb.get
def delete_single_object(request, pid):
  '''Note: The semantics for this method are different than for the production
  method that deletes an object. This method removes all traces that the object
  ever existed.
  '''
  _delete_object(pid)
  return service.view_shared.http_response_with_boolean_true_type()


def _delete_object(pid):
  #service.view_asserts.object_exists(pid)
  sciobj = service.models.ScienceObject.objects.get(pid=pid)
  # If the object is wrapped, only delete the reference. If it's managed, delete
  # both the object and the reference.
  url_split = urlparse.urlparse(sciobj.url)
  if url_split.scheme == 'file':
    sciobj_path = service.util.store_path(settings.OBJECT_STORE_PATH, pid)
    try:
      os.unlink(sciobj_path)
    except EnvironmentError:
      pass
  # At this point, the object was either managed and successfully deleted or
  # wrapped and ignored. The SysMeta object is left orphaned in the filesystem
  # to be cleaned by an asynchronous process later. If the same object that
  # was just deleted is recreated, the old SysMeta object will be overwritten
  # instead of being cleaned up by the async process.
  #
  # Delete the DB entry.
  #
  # By default, Django's ForeignKey emulates the SQL constraint ON DELETE
  # CASCADE. In other words, any objects with foreign keys pointing at the
  # objects to be deleted will be deleted along with them.
  #
  # TODO: This causes associated permissions to be deleted, but any subjects
  # that are no longer needed are not deleted. The orphaned subjects should
  # not cause any issues and will be reused if they are needed again.
  sciobj.delete()


# ------------------------------------------------------------------------------
# Event Log.
# ------------------------------------------------------------------------------

def delete_event_log(request):
  service.models.EventLog.objects.all().delete()
  service.models.EventLogIPAddress.objects.all().delete()
  service.models.EventLogEvent.objects.all().delete()
  return service.view_shared.http_response_with_boolean_true_type()


@service.restrict_to_verb.post
def inject_fictional_event_log(request):
  service.view_asserts.post_has_mime_parts(request, (('file', 'csv'),))

  # Create event log entries.
  csv_reader = csv.reader(request.FILES['csv'])

  for row in csv_reader:
    pid = row[0]
    event = row[1]
    ip_address = row[2]
    user_agent = row[3]
    subject = row[4]
    timestamp = d1_common.date_time.from_iso8601((row[5]))
    #member_node = row[6]

    # Create fake request object.
    request.META = {
      'REMOTE_ADDR': ip_address,
      'HTTP_USER_AGENT': user_agent,
      'REMOTE_ADDR': subject,
      'SERVER_NAME': 'dataone.org',
      'SERVER_PORT': '80',
    }

    service.event_log._log(pid, request,
                      event, d1_common.date_time.strip_timezone(timestamp))

  return service.view_shared.http_response_with_boolean_true_type()