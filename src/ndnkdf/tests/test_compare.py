#
# Copyright (c) 2012, 2013 NORDUnet A/S
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#     1. Redistributions of source code must retain the above copyright
#        notice, this list of conditions and the following disclaimer.
#     2. Redistributions in binary form must reproduce the above
#        copyright notice, this list of conditions and the following
#        disclaimer in the documentation and/or other materials provided
#        with the distribution.
#     3. Neither the name of the NORDUnet nor the names of its
#        contributors may be used to endorse or promote products derived
#        from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Author : Fredrik Thulin <fredrik@thulin.net>
#

import platform

if platform.python_version() < '2.7':
    import unittest2 as unittest
else:
    import unittest

import hmac as HMAC
from hashlib import sha512 as SHA512

import ndnkdf


class TestCompare(unittest.TestCase):

    """
    Compare all permutations of key-salt-iterations between the NDNKDF implementation
    and another one used as reference.

    The other PBKDF2 implementation should be, or be compatible with, the one found at
    https://www.dlitz.net/software/python-pbkdf2/
    """

    keys = [
        '',
        chr(0) * 8,
        chr(0) * 64,
        chr(0) * 100,
        'passwd',
        'This is a secret passphrase.',
        'pass\0word',
        'a',
        'a' * 32,
    ]
    salts = [
        '',
        chr(0) * 8,
        'saltSALTsaltSALTsalt',
        'NaCL',
        'a',
        'a' * 32,
    ]
    iterations = [1, 5, 100, 256]

    def setUp(self):
        self.ndnkdf = ndnkdf.NDNKDF()
        # This refers to the Python PBKDF2 implementation found at
        # https://www.dlitz.net/software/python-pbkdf2/ - It is imported here
        # to have only these tests fail if it is not present - not the whole
        # test suite.
        try:
            from pbkdf2 import PBKDF2
        except ImportError:
            import sys

            sys.stderr.write("python-pbkdf2 not available, get it from https://www.dlitz.net/software/python-pbkdf2/\n")
            sys.exit(1)
        self.other_pbkdf2 = PBKDF2

    def test_and_compare_values(self):
        """ Test and compare result with other PBKDF2 implementation. """
        for key in self.keys:
            for salt in self.salts:
                for iteration in self.iterations:
                    nettle_res = self.ndnkdf.pbkdf2_hmac_sha512(key, iteration, salt)
                    other_res = self.other_pbkdf2(
                        key, salt, iterations=iteration, macmodule=HMAC, digestmodule=SHA512
                    ).read(self.ndnkdf._DIGEST_SIZE)
        self.assertEquals(nettle_res, other_res)
