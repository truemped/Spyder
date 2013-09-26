# vim: set fileencoding=utf-8 :
#
# Copyright (c) 2013 Daniel Truemper <truemped at googlemail.com>
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
#
#
from __future__ import absolute_import, division, print_function, with_statement

import pytest

from spyder.api.uri import CrawledUri
from spyder.core.worker.processors.stripparams import StripParamsProcessor


def test_initializing_works():
    p = StripParamsProcessor()
    assert p._params == ['jsessionid', 'phpsessid', 'aspsessionid', 'sid']


@pytest.mark.parametrize(('url', 'expected'), [
    ('http://localhost', 'http://localhost'),
    ('http://localhost?id=5', 'http://localhost?id=5'),
    ('http://localhost/?id=5&sid=4&format=uml',
        'http://localhost/?id=5&format=uml'),
    ('http://localhost/?id=5&jsessionid=4&format=uml',
        'http://localhost/?id=5&format=uml'),
    ('http://localhost/?id=5&phpsessid=4&format=uml',
        'http://localhost/?id=5&format=uml'),
    ('http://localhost/?id=5&aspsessionid=4&format=uml',
        'http://localhost/?id=5&format=uml'),
    ])
def test_param_extraction_works(url, expected):
    p = StripParamsProcessor()
    result = p._strip_link(url)
    assert result == expected


def test_processor_workflow():
    ccuri = CrawledUri()
    ccuri.url = 'http://localhost'
    ccuri.links = ['http://localhost/?id=5&aspsessionid=4&format=uml',
                   'http://localhost/?id=5&phpsessid=4&format=uml',
                   'http://localhost/?id=5'
                  ]

    p = StripParamsProcessor()
    ccuri = p.execute(ccuri)
    assert isinstance(ccuri, CrawledUri)
    assert ccuri.url == 'http://localhost'
    assert ccuri.links == ['http://localhost/?id=5&format=uml',
                   'http://localhost/?id=5&format=uml',
                   'http://localhost/?id=5'
                  ]
