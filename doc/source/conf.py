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
"""Sphinx configuration for DataONE Python Products documentation
"""

import sys
import os

project = u'DataONE Python Products'
copyright = u'2016 Participating institutions in DataONE'

autosummary_generate = False

extensions = [
  'sphinx.ext.autodoc',
  'sphinx.ext.doctest',
  'sphinx.ext.todo',
  'sphinx.ext.graphviz',
  'sphinx.ext.autosummary',
  'sphinx.ext.pngmath',
  'sphinx.ext.ifconfig',
  'sphinx.ext.inheritance_diagram',
  'sphinx.ext.extlinks',
]

source_suffix = '.rst'
master_doc = 'index'
version = ''
release = ''
exclude_trees = ['_build', '_templates']
pygments_style = 'sphinx'
today_fmt = '%Y-%m-%d'

# Theme

html_logo = 'dataone_logo.png'

# html_theme = 'dataone'
# html_theme_options = {
#   'collapsiblesidebar': 'true',
#   'render_epad_comments': 'false',
# }
# html_theme_path = ['../docutils/sphinx_themes',]


from better import better_theme_path
html_theme_path = [better_theme_path]
html_theme = 'better'