.. sbspk documentation master file, created by
   sphinx-quickstart on Fri Mar 25 11:38:47 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

SBSPK library
=================================

.. automodule:: sbspk


.. autoclass:: sbspk.SBSPK
   :members:
   
   .. autoattribute:: email
      
      Email address required by Horizons SPK generation.

   .. autoattribute:: fileformat
   
      Kernel file name format. ``<OBJID>`` will be replaced with 
      current object ID, ``<TARGET>`` will be replaced with specified
      targe name. Be carefull - files will be overwritten without 
      any warning
    
   .. autoattribute:: startdate
   
      Ephemeris start date for an SPK file, default is ``'2010-01-01'``. 

   .. autoattribute:: stopdate
   
      Ephemeris stop date for an SPK file, default is ``'2040-01-01'``.
      
      
   .. autoattribute:: printprogress
   
      Prints the SPK download progress meter. This is separate from 
      logging and turned off by default.
   
   .. autoattribute:: timeout
   
      Max time to wait for an expected JPL Horizons output (seconds).
      After this a ``pexpect.TIMEOUT`` exception will be thrown. 

.. autoexception:: sbspk.SBSPKError

.. autofunction:: sbspk._sbspk.talk


Command line tool
=========================
.. automodule:: sbspk.command_line


.. argparse::
   :module: sbspk.command_line
   :func: _get_argparser
   :prog: sbspk
   :nodefault:


.. toctree::
   :maxdepth: 2
   
   

