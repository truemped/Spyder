#
# Copyright (c) 2011 Daniel Truemper truemped@googlemail.com
#
# encoding.py 09-Feb-2011
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


def get_content_type_encoding(curi):
    """
    Determine the content encoding based on the `Content-Type` Header.

    `curi` is the :class:`CrawlUri`.
    """
    content_type = 'text/plain'
    charset = ''

    if curi.rep_header and 'Content-Type' in curi.rep_header:
        (content_type, charset) = extract_content_type_encoding(
                curi.rep_header['Content-Type'])

    if charset == '' and curi.content_body:
        (_, e) = _detect_from_body(curi.content_body[:512].lower())

        if not e:
            # there was no information in the first 512 bytes,  try the whole text
            (_, e) = _detect_from_body(curi.content_body.lower())

        charset = e

    if charset == '' and curi.content_body:
        # wow, still no information, maybe check the byte order mark
        if curi.content_body[:3] == '\xef\xbb\xbf':
            charset = 'utf-8'

    return (content_type, charset)


def _detect_from_body(body):
    """
    Try to detect the encoding from the body.
    """
    # no charset information in the http header
    ctypestart = body.find('content-type')
    if ctypestart != -1:
        # there is a html header
        ctypestart = body.find('content="', ctypestart)
        ctypeend = body.find('"', ctypestart + 9)
        return extract_content_type_encoding(
                body[ctypestart + 9:ctypeend])

    charsetstart = body.find('charset="')
    if charsetstart != -1:
        # there is a charset header
        charsetstart = body.find('charset="', charsetstart)
        charsetend = body.find('"', charsetstart + 9)
        return (None, body[charsetstart + 9: charsetend])

    return (None, None)


def extract_content_type_encoding(content_type_string):
    """
    Extract the content type and encoding information.
    """
    charset = ''
    content_type = ''
    for part in content_type_string.split(';'):
        part = part.strip().lower()
        if part.startswith('charset'):
            charset = part.split('=')[1]
            charset = charset.replace('-', '_')
        else:
            content_type = part

    return (content_type, charset)
