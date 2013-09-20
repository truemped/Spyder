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
from abc import ABCMeta, abstractmethod

from spyder._compat import with_metaclass


class StoredQueue(with_metaclass(ABCMeta, object)):
    '''
    Abstraction for storing URL queues.
    '''

    @abstractmethod
    def close(self):
        '''
        Close the db.
        '''

    @abstractmethod
    def __contains__(self, curi):
        '''Check whether the `curi` is known.

        :param curi: the current crawl uri
        :type curi: spyder.api.uri.CrawlUri
        :return: `True` if the URL is known, `False` otherwise
        :rtype: bool
        '''

    @abstractmethod
    def add_or_update(self, curi):
        '''Add or update a `curi`.

        :param curi: the current crawl uri
        :type curi: spyder.api.uri.CrawlUri
        '''

    @abstractmethod
    def remove(self, curi):
        '''Remove a `curi` from the queues.

        :param curi: the current crawl uri
        :type curi: spyder.api.uri.CrawlUri
        '''

    @abstractmethod
    def ignore(self, curi):
        '''Ignore a `curi` from no on.

        :param curi: the current crawl uri
        :type curi: spyder.api.uri.CrawlUri
        '''
