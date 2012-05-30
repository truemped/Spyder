# vim: set fileencoding=utf-8 :
#
# Copyright (c) 2011 Daniel Truemper <truemped at googlemail.com>
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
"""
More general processor to strip specific query parts from extracted urls.
"""
from spyder.core.constants import CURI_EXTRACTED_URLS


class StripQueryParams(object):
    """
    Simple processor to remove specific query params from extracted urls.
    """

    def __init__(self, settings):
        """
        Initialize me.
        """
        self._query_params = settings.REMOVE_QUERY_NAMES

    def __call__(self, curi):
        """
        Main method stripping the session stuff from the query string.
        """
        if CURI_EXTRACTED_URLS not in curi.optional_vars:
            return curi

        urls = []
        for raw_url in curi.optional_vars[CURI_EXTRACTED_URLS].split('\n'):
            urls.append(self._remove_query_params(raw_url))

        curi.optional_vars[CURI_EXTRACTED_URLS] = "\n".join(urls)
        return curi

    def _remove_query_params(self, raw_url):
        """
        Remove the session information.
        """
        for param in self._query_params:
            url = raw_url.lower()
            begin = url.find(param)
            while begin > -1:
                end = url.find('&', begin)
                if end == -1:
                    raw_url = raw_url[:begin]
                else:
                    raw_url = "%s%s" % (raw_url[:begin], raw_url[end:])
                url = raw_url.lower()
                begin = url.find(param)

        return raw_url
