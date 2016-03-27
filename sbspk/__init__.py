#!/usr/bin/env python3
"""
``sbspk`` is a Python module for retrieving small-body (asteroids, comets) SPICE SPK kernels from the JPL Horizons system.

The ``sbspk.SBSPK`` class automates the above:

>>> from sbspk import SBSPK
>>> s = SBSPK()
>>> s.startdate = '2016-01-01'
>>> s.stopdate = '2018-06-01'
>>> kernels = s.get(['2014 SU1', '2015 TB', '2000 SG344'], directory='/tmp')
>>> kernels
[('/tmp/3689273_2014_SU1.bsp', '3689273'), 
 ('/tmp/3728897_2015_TB.bsp', '3728897'),
 ('/tmp/3054374_2000_SG344.bsp', '3054374')]
 
Currently only single-object binary kernels are supproted.
``sbspk`` provides also a simple command line utility 
under the same name.

"""
from ._sbspk import SBSPK, SBSPKError
