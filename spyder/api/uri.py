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

from schematics.models import Model
from schematics.types import StringType, IntType, BooleanType, DateTimeType
from schematics.types.compound import ModelType, ListType


class CrawlUri(Model):
    '''Simple model storing information about URIs to be crawled and their
    crawl history.
    '''
    url = StringType(required=True)
    crawled_timestamps = ListType(IntType())
    changes_detected = ListType(IntType())
    last_modified = IntType()
    etag = StringType()
    ignored = BooleanType()


class ResponseHeaders(Model):
    '''Response headers that are used in the crawler logic.'''
    location = StringType()
    date = DateTimeType()
    expires = DateTimeType()
    cache_control = StringType()
    last_modified = DateTimeType()
    etag = StringType()
    content_type = StringType()

    @classmethod
    def from_headers(cls, headers):
        h = cls()
        h.location = headers.get('Location', None)
        h.etag = headers.get('Etag', None)
        h.content_type = headers.get('Content-Type', None)
        h.date = headers.get('Date', None)
        h.expires = headers.get('Expires', None)
        h.last_modified = headers.get('Last-Modified', None)
        h.cache_control = headers.get('Cache-Control', None)
        return h


class CrawledUri(CrawlUri):
    '''A crawled uri also contains some metadata and the contents from the
    stored page.
    '''
    links = ListType(StringType())
    resp_headers = ModelType(ResponseHeaders)
    resp_body = StringType()
    resp_code = IntType()

    @classmethod
    def from_curi(cls, curi):
        '''Construct a *crawled* uri from the :class:`CrawlUri`.'''
        return cls(**curi.validate())
