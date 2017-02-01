Fast PBKDF2 in Python

Copyright (c) 2012, NORDUnet A/S
See the file COPYING for license statement.

NDNKDF exposes the PBKDF2-HMAC-SHA512 functionality of Nettle in Python.

It is about 25x faster than python-pbkdf2.

==============
 Installation
==============

  $ python setup.py test
  $ sudo python setup.py install

The PBKDF2 function was added to Nettle at 2012-09-12 (first released with
Nettle 2.6, SO version 4.4). It is possible to have libnettle.so in a non-
standard location and set the environment variable NDNKDF_PATH acccordingly
(something like `NDNKDF_PATH=/path/to/nettle/lib python setup.py test`).

Sometime between version 2.6 and 3.2, Nettle changed to using size_t's.
This made Python dump core, and ndnkdf has been changed to use size_t's
which means it probably doesn't work with older Nettle now.

=============
 Basic usage
=============

  import ndnkdf

  n = ndnkdf.NDNKDF()
  print n.pbkdf2_hmac_sha512('passwd', 1, 'salt').encode('hex')

=============
 Performance
=============

examples/pbkdf2-plot can be used to compare NDNKDF with python-pbkdf2 (the
one available at https://www.dlitz.net/software/python-pbkdf2/).

If the numpy and matplotlib python modules are installed, a graph will be shown.

This is the benchmark results on an Intel(R) Core(TM) i5-2430M CPU @ 2.40GHz :

    PBKDF2-HMAC-SHA512 benchmark result :

      N=    16 -> Python ==     0 ms, Nettle ==     0 ms
      N=    32 -> Python ==     1 ms, Nettle ==     0 ms
      N=    64 -> Python ==     2 ms, Nettle ==     0 ms
      N=   128 -> Python ==     4 ms, Nettle ==     0 ms
      N=   256 -> Python ==     8 ms, Nettle ==     0 ms
      N=   512 -> Python ==    16 ms, Nettle ==     0 ms
      N=  1024 -> Python ==    33 ms, Nettle ==     1 ms
      N=  2048 -> Python ==    66 ms, Nettle ==     2 ms
      N=  4096 -> Python ==   131 ms, Nettle ==     5 ms
      N=  8192 -> Python ==   260 ms, Nettle ==    11 ms
      N= 16384 -> Python ==   515 ms, Nettle ==    21 ms

