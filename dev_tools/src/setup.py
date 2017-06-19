#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2013 DataONE
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
"""DataONE developer tools package
"""

from __future__ import absolute_import

import setuptools


def main():
  setuptools.setup(
    name='dataone.dev',
    version='2.3.0rc1',
    description='DataONE developer tools',
    author='DataONE Project',
    author_email='developers@dataone.org',
    url='https://github.com/DataONEorg/d1_dev',
    license='Apache License, Version 2.0',
    packages=setuptools.find_packages(),
    include_package_data=True,
    exclude_package_data={
      '': ['settings.py'],
    },
    install_requires=[
      # These are not yet available when bootstrapping on Travis
      #'dataone.cli == 2.3.0rc1',
      #'dataone.common == 2.3.0rc1',
      #'dataone.libclient == 2.3.0rc1',
      #
      'baron == 0.6.5',
      'pip == 9.0.1',
      'redbaron == 0.6.3',
    ],
    setup_requires=[
      'setuptools_git >= 1.1',
    ],
    classifiers=[
      'Development Status :: 5 - Production/Stable',
      'Intended Audience :: Developers',
      'Topic :: Scientific/Engineering',
      'License :: OSI Approved :: Apache 2.0 License',
      'Programming Language :: Python :: 2',
      'Programming Language :: Python :: 2.7',
    ],
    keywords='DataONE python'
  )


if __name__ == '__main__':
  main()