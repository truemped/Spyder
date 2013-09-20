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

from spyder._compat import with_metaclass


class AbstractProcessor(with_metaclass(ABCMeta, object)):
    '''Base class for implementing crawl processors.

    A processor is part of the processor chain executed in the worker. Within
    the worker basically everything is a processor, i.e. the fetcher is as
    much as a processor as the class for dumping the crawled contents.
    '''

    @abstractmethod
    def execute(self, curi):
        '''Execute the processor with the `curi`.

        In contrast to the frontier `curis`, `curis` in the worker also contain
        all information about the (to be) downloaded components as well as all
        information about the download itself like the server response time,
        e.g.
        '''
