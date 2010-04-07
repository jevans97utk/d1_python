#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  :mod:`models` -- URLs
========================

:module: urls
:platform: Linux
:synopsis: URLs

.. moduleauthor:: Roger Dahl
"""

from django.conf.urls.defaults import *

# Enable admin.
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
  'mn_prototype.mn_service.views',
  # CN interface.

  # /object/
  (r'^object/$', 'object_collection'),
  (r'^object/(.*)$', 'object_contents'),
  (r'^object/(.*)/meta$', 'object_sysmeta'),

  # /log/
  (r'^log/$', 'access_log_view'),

  # D1 adapter interface.
  (r'^register/$', 'register'),

  # Diagnostic / Debugging.
  (r'^get_ip/$', 'auth_test'),

  # Admin.
  (r'^admin/doc/', include('django.contrib.admindocs.urls')),
  (r'^admin/', include(admin.site.urls)),
)
