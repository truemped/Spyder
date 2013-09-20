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

from abc import ABCMeta, abstractmethod

import logging
from Queue import PriorityQueue, Empty

from tornado.options import options

from spyder._compat import with_metaclass


class AbstractBaseFrontier(with_metaclass(ABCMeta, object)):
    '''A base class for implementing frontiers.

    Basically this class provides the different general methods and
    configuration parameters used for frontiers.
    '''

    def __init__(self, backend_queues, unique_uri_filter):
        '''Initialize the frontier.'''
        # logging
        self._logger = logging.getLogger(__name__)

        # the heap
        self._heap = PriorityQueue(maxsize=options.frontier_heap_size)
        self._heap_min_size = options.frontier_heap_min
        self._running = False

        # the backend queues
        self._backend_queues = backend_queues

        # filter for uri uniqueness
        self._unique_uri_filter = unique_uri_filter

        # dictionary of uris currently being crawled
        self._current_uris = {}

    def close(self):
        '''Stop the frontier from crawling anything anymore and close the queue
        db eventually.
        '''
        self._running = False
        self._backend_queues.close()

    def add_url(self, curi):
        '''Add the specified :class:`spyder.api.uri.CrawlUri` to the frontier.
        '''
        if curi in self._unique_uri_filter:
            # we already know this uri
            self._logger.debug("Trying to update a known uri... " + \
                    "(%s)" % (curi.url,))
            return

        self._logger.info("Adding '%s' to the frontier" % curi.url)
        self._unique_uri_filter.add(curi)
        self._backend_queues.add_or_update(curi)

    def add_to_heap(self, curi, priority):
        '''Add a URI to the heap in order to download it.'''
        self._logger.debug('Adding %s to the heap' % curi.url)
        self._heap.put_nowait((priority, curi))
        self._current_uris[curi.url] = curi

    def update_url(self, curi):
        '''Update a known url after it has been crawled, e.g.'''
        self._front_end_queues.add_or_update(curi)

    def ignore_uri(self, curi):
        '''Ignore a :class:`spyder.api.uri.CrawlUri` from now on.'''
        curi.ignored = True
        self._front_end_queues.ignore(curi)

    def next(self):
        '''
        Return the next URL to be crawled.
        '''
        if self._heap.qsize() < self._heap_min_size:
            self.update_heap()
        try:
            (_, curi) = self._heap.get_nowait()
            return curi
        except Empty:
            # nothing to crawl
            return None

    @abstractmethod
    def update_heap(self):
        '''Update the heap and add URLs that can be crawled right away.
        '''

    @abstractmethod
    def process_successful_crawl(self, curi):
        '''Called when an url was crawled successfully, i.e. had a HTTP status
        code of 20x.

        :param curi: the url that was crawled
        :type curi: :class:`spyder.api.uri.CrawlUri`
        '''

    @abstractmethod
    def process_error(self, curi):
        '''Called when an url had errors during downloading, i.e. had a HTTP
        status code of 30x, 40x, 50x or even worst.

        :param curi: the url that was crawled
        :type curi: :class:`spyder.api.uri.CrawlUri`
        '''
