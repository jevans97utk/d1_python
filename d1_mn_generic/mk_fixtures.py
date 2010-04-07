#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  mk_fixtures
==============

:module: mk_fixtures
:platform: Linux
:synopsis: mk_fixtures

.. moduleauthor:: Roger Dahl
"""

import sys
import os

import settings

# Empty fixture.

f = open(os.path.join(settings.FIXTURE_DIRS, 'empty.fixture.json'), 'w')
f.write('[]')
f.close()

# Populated fixture.

# Populate db with information about filesystem objects.
if 'reset' in sys.argv:
  print os.system('rm test_db.sq3')
  print os.system('./manage.py syncdb')
  print os.system('./manage.py update_db')
  print os.system('./manage.py insert_test_log')

# Update the test fixture to match.
print os.system(
  './manage.py dumpdata mn_service > %s' % os.path.join(
    settings.FIXTURE_DIRS, 'base.fixture.json'
  )
)
