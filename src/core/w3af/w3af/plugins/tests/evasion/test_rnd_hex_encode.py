"""
test_rnd_hex_encode.py

Copyright 2012 Andres Riancho

This file is part of w3af, http://w3af.org/ .

w3af is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

w3af is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with w3af; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""
import unittest

from w3af.core.data.parsers.doc.url import URL
from w3af.core.data.url.HTTPRequest import HTTPRequest
from w3af.plugins.evasion.rnd_hex_encode import rnd_hex_encode


class TestEvasion(unittest.TestCase):
    def test_no_modification(self):
        rhe = rnd_hex_encode()

        u = URL('http://www.w3af.com/')
        r = HTTPRequest(u)
        self.assertEqual(rhe.modify_request(r).url_object.url_string,
                         u'http://www.w3af.com/')

    def test_encode_path_case01(self):
        rhe = rnd_hex_encode()

        u = URL('http://www.w3af.com/a/')
        r = HTTPRequest(u)
        modified_path = rhe.modify_request(r).url_object.get_path()
        self.assertIn(modified_path, ['/a/', '/%61/'])

    def test_encode_path_case02(self):
        rhe = rnd_hex_encode()

        u = URL('http://www.w3af.com/aa/')

        r = HTTPRequest(u)
        modified_path = rhe.modify_request(r).url_object.get_path()
        self.assertIn(modified_path, ['/aa/', '/%61a/', '/a%61/', '/%61%61/'])

        #
        #    The plugins should not modify the original request
        #
        self.assertEqual(u.url_string,
                         u'http://www.w3af.com/aa/')

    def test_encode_post_data(self):
        rhe = rnd_hex_encode()

        u = URL('http://www.w3af.com/')
        r = HTTPRequest(u, data='a=b')
        modified_pdata = rhe.modify_request(r).get_data()
        self.assertIn(modified_pdata, ['a=b', '%61=b', 'a=%62', '%61=%62'])
