#
# Copyright (c) 2008 Daniel Truemper truemped@googlemail.com
#
# setup.py 04-Jan-2011
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# under the License.
#
#

from imp import load_source
import os
from setuptools import setup
import sys


init = load_source('init', os.path.join('spyder', '__init__.py'))
PY2 = sys.version_info[0] == 2

long_description = open("README.rst").read()

tests_require = [
    'mock',
    'pytest',
    'pytest-cov',
]

if sys.version_info < (2, 7):
    tests_require.append('unittest2')


extras_require = {}
extras_require['test'] = tests_require
extras_require['futures'] = ''
if PY2:
    extras_require['futures'] = 'futures == 2.1.3'


setup (
    name='spyder',
    version='.'.join([str(v) for v in init.__version__]),

    author='Daniel Truemper',
    author_email='truemped@gmail.com',
    url='http://spyder.readthedocs.org/',
    license="http://www.apache.org/licenses/LICENSE-2.0",
    description = "A python spider",
    long_description = long_description,

    packages=['spyder'],

    install_requires=[
        'tornado >= 3.1.0',
        'schematics >= 0.6.0',
        'scales >= 1.0.3',
        'pyzmq >= 13.1.0',
    ],
    tests_require=tests_require,
    extras_require=extras_require,

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
    ]
)
