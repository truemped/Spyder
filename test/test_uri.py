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

from schematics.exceptions import ValidationError

from spyder.api.uri import CrawlUri, CrawledUri, ResponseHeaders


def test_that_crawled_uri_construction_works():
    curi = CrawlUri()
    curi.url = 'http://localhost'

    ccuri = CrawledUri.from_curi(curi)
    assert ccuri.url == curi.url


def test_simple_curi_validation():
    curi = CrawlUri()

    with pytest.raises(ValidationError):
        curi.validate()


def test_ccuri_with_invalid_curi():
    curi = CrawlUri()

    with pytest.raises(ValidationError):
        CrawledUri.from_curi(curi)


def test_ccuri_with_headers():
    ccuri = CrawledUri()
    resp_headers = ResponseHeaders(location='http://test')
    ccuri.resp_headers = resp_headers

    assert ccuri.resp_headers.location == 'http://test'
