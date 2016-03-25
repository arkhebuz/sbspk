#!/usr/bin/env python3
"""
Retrieve small body SPICE SPK kernels from the JPL Horizons system.

This package provides an SBSPK class that automates the above:

>>> from sbspk import SBSPK
>>> s = SBSPK()
>>> s.startdate = '2016-01-01'
>>> s.stopdate = '2018-06-01'
>>> kernels = s.get(['2014 SU1', '2015 TB', '2000 SG344'], directory='/tmp')
"""
from ._sbspk import SBSPK, SBSPKError
