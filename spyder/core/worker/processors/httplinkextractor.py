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

import urlparse

from spyder.api.processor import AbstractProcessor


class HttpLinkExtractor(AbstractProcessor):
    '''Simple processor that will extract links from the HTTP **Location**
    header.'''

    def execute(self, ccuri):
        '''Execute this processor and extract any location headers.'''
        if (ccuri.resp_code in [301, 302] and
                ccuri.resp_headers and
                ccuri.resp_headers.location):

            link = ccuri.resp_headers.location

            if link.find("://") == -1:
                # a relative link. this is bad behaviour, but yeah, you know...
                link = urlparse.urljoin(ccuri.url, link)

            if not ccuri.links:
                ccuri.links = []

            ccuri.links.append(link)

        return ccuri
