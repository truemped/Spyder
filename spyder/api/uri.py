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
from schematics.types import StringType, IntType, BooleanType
from schematics.types.compound import DictType, ListType


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


class CrawledUri(CrawlUri):
    '''A crawled uri also contains some metadata and the contents from the
    stored page.
    '''
    links = ListType(StringType())
    resp_headers = DictType()
    resp_body = StringType()

    @classmethod
    def from_curi(cls, curi):
        '''Construct a *crawled* uri from the :class:`CrawlUri`.'''
        return cls(**curi.validate())
