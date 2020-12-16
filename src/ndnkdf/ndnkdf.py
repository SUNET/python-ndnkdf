#
# Copyright (c) 2012, 2013, 2017 NORDUnet A/S
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

import ctypes
import ctypes.util
import os


class NDNKDF_Error(Exception):
    pass


class NDNKDF_LibraryError(NDNKDF_Error):
    pass


class NDNKDF:

    _DIGEST_SIZE = 64

    """
    NORDUnet Key Derivation Function

    Really just a version of PBKDF2-HMAC-SHA512 using libnettle for speed.
    """

    def __init__(self, path=None):
        if path is None:
            path = os.environ.get('NDNKDF_PATH')
        if path is not None:
            self.name = os.path.join(path, 'libnettle.so')
        else:
            self.name = ctypes.util.find_library('nettle')
        self.nettle = ctypes.cdll.LoadLibrary(self.name)
        # check for the functions we use - the PBKDF2 function was added 2012-09-12
        # (appeared in Nettle version 2.6, SO version 4.4).
        for func in [
            'nettle_hmac_sha512_set_key',
            'nettle_hmac_sha512_update',
            'nettle_hmac_sha512_digest',
            'nettle_pbkdf2',
        ]:
            if not hasattr(self.nettle, func):
                raise NDNKDF_LibraryError('Nettle library missing function {!s}()'.format(func))

    def pbkdf2_hmac_sha512(self, key: bytes, iterations: int, salt: bytes) -> bytes:
        """
        Invoke nettle PBKDF2 using HMAC-SHA-512 on key, iterations and salt.
        """
        buf = ctypes.create_string_buffer(b'', size=self._DIGEST_SIZE)
        # sha512ctx is a C struct consisting of three sha512_ctx. I calculate them to be
        # 148 bytes each, but let's just fake it with an opaque buffer of 1024 bytes.
        sha512ctx = ctypes.create_string_buffer(b'', size=1024)
        self.nettle.nettle_hmac_sha512_set_key(ctypes.byref(sha512ctx), ctypes.c_size_t(len(key)), key)
        self.nettle.nettle_pbkdf2(
            ctypes.byref(sha512ctx),
            self.nettle.nettle_hmac_sha512_update,
            self.nettle.nettle_hmac_sha512_digest,
            ctypes.c_size_t(self._DIGEST_SIZE),
            int(iterations),
            ctypes.c_size_t(len(salt)),
            salt,
            ctypes.c_size_t(self._DIGEST_SIZE),
            ctypes.byref(buf),
        )
        return buf.raw
