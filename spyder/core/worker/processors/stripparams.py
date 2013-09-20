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

from urllib import urlencode
from urlparse import parse_qsl, urlparse, urlunparse

from tornado.options import define

from spyder.api.processor import AbstractProcessor


define('proc_strip_params', multiple=True, default=['jsessionid',
       'phpsessid', 'aspsessionid', 'sid'],
       help='A list of query params to remove from extracted urls.')


class StripParamsProcessor(AbstractProcessor):
    '''Simple processor that removes a configurable list of query params from
    extracted URLs.
    '''

    def __init__(self):
        '''Initialize the processor.'''
        from tornado.options import options
        self._params = options.proc_strip_params

    def execute(self, ccuri):
        '''Execute this processor.'''
        stripped_links = [self._strip_link(link) for link in ccuri.links]
        ccuri.links = stripped_links
        return ccuri

    def _strip_link(self, link):
        '''Remove the selected params from the link.'''
        parsed = urlparse(link)
        params = parse_qsl(parsed.query)
        params = [param for param in params if param[0] not in self._params]
        return urlunparse((parsed[0], parsed[1], parsed[2], parsed[3],
                           urlencode(params), parsed[5]))
