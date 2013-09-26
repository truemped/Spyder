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

from spyder.api.uri import CrawledUri, ResponseHeaders
from spyder.core.worker.processors.httplinkextractor import HttpLinkExtractor


def test_initializing_works():
    HttpLinkExtractor()
    assert True


@pytest.mark.parametrize(('url', 'code', 'location', 'expected'), [
        ('http://localhost', 200, 'http://localhost/test', None),
        ('http://localhost', 302, 'http://localhost/test',
            ['http://localhost/test']),
        ('http://localhost', 301, 'http://localhost/test',
            ['http://localhost/test']),
        ('http://localhost', 301, '/test',
            ['http://localhost/test']),
        ('http://localhost', 304, 'http://localhost/test', None),
    ]
)
def test_http_link_extractor(url, code, location, expected):
    headers = ResponseHeaders(location=location)
    ccuri = CrawledUri(url=url, resp_code=code, resp_headers=headers)

    p = HttpLinkExtractor()
    p.execute(ccuri)

    assert ccuri.links == expected
