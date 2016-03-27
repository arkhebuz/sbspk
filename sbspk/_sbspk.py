#!/usr/bin/env python3
"""
Retrieve small body SPICE SPK kernels from the JPL Horizons system.

http://ssd.jpl.nasa.gov/?horizons_doc#spk
"""
import os
import re
import sys
import pexpect
import logging
import argparse
from urllib.request import urlretrieve


class SBSPKError(Exception):
    ''' Exception raised by SBSPK code. 
    
    Custom exception allows to differentiate bettewen those intentionaly
    raised from SBSPK with raise statement and other errors. This
    exception is exposed at module level for convenience, so you can 
    import it with:
    
    >>> from sbspk import SBSPKError
    '''
    pass


def __talk_function_demo(target, email, startdate, stopdate, timeout):
    ''' Short demo of a talk function protocol'''
    FTPURL = 'ftp://none.none'
    OBJID = '12345678'
    
    raise SBSPKError('Error message')
    return FTPURL, OBJID


def talk(target, email, startdate, stopdate, timeout):
    '''
    "Talks" to the JPL Horizons over the telnet interface to generate single small-body SPICE kernel.
    
    This function is hidden from normal package-level API. If everything
    works, just use an SBSPK class. If retrieval is broken, it's probably
    broken in this function, hence it's included in the documentation.
    
    Arguments:
        target (str): Name of a target object.
        email (str): Your email address.
        startdate (str): Ephemeris start date for an SPK file, for example ``'2010-01-01'``.
        stoptdate (str): Ephemeris stop date for an SPK file, for example ``'2040-01-01'``.
        timeout (int): Max time to wait for expected JPL Horizons output, seconds.
    
    Raises:
        pexpect.TIMEOUT: ``timeout`` was reached. Aside of network connectivity
                         problems may indicate Horizons interface change.
        sbspk.SBSPKError: Raised if either ``target`` was not found or object ID
                          could not be extracted from the telnet output.
    
    Returns:
        FTPURL (str): Full ftp address of a generated binary SPK file for download.
        OBJID (str): Horizons system object ID.
    
    This function makes a quite heavy use of a logging at the DEBUG level 
    to capture most of its communication.
    '''
    logger = logging.getLogger("SBSPK_TalkLogger")
    # Spawn telnet-horizons process which we will control with pexpect
    th = pexpect.spawn('telnet horizons.jpl.nasa.gov 6775')
    ex = th.expect
    sl = th.sendline
    dt = timeout
    
    # Wait for Horizons prompt
    ex('Horizons>', timeout=dt)
    logger.debug(str(th.before))
    logger.debug("MATCH: "+str(th.after))

    sl('PAGE')
    ex(['PAGING toggled OFF'], timeout=dt)
    logger.debug(str(th.before))
    logger.debug("MATCH: " + str(th.after))
    
    # Send target body name to Horizons
    sl(target)
    
    # Horizons will ask if you want to proceed with search
    ex(['Continue'], timeout=dt)
    logger.debug(str(th.before))
    logger.debug("MATCH: " + str(th.after))
    sl('yes')

    rtn = ex(['\[S]PK', 'No matches found'], timeout=dt)
    logger.debug(str(th.before))
    logger.debug("MATCH: " + str(th.after))
    if rtn == 1:
        logger.error('No match found for ' + target)
        raise SBSPKError('No match found for ' + target)
    sl('s')

    # Before email address prompt there's printed object ID
    ex(['Enter your Internet e-mail address'], timeout=dt)
    logger.debug(str(th.before))
    logger.debug("MATCH: " + str(th.after))

    # Parse pe.before to extract object ID
    pattern = re.compile('.*object ID: *(?P<OBJID>[0-9]*)')
    m = pattern.match(str(th.before))
    if m is not None:
        OBJID = m.group('OBJID')
        logger.info("Object ID: " + OBJID)
    else:
        raise SBSPKError('Cannot parse object ID')

    sl(email)
    
    ex(['Confirm e-mail address'], timeout=dt)
    logger.debug(str(th.before))
    logger.debug("MATCH: " + str(th.after))
    sl('yes')
    
    ex(['SPK text transfer format'], timeout=dt)
    logger.debug(str(th.before))
    logger.debug("MATCH: " + str(th.after))
    sl('NO')
    
    rtn = ex(['SPK object START'], timeout=dt)
    logger.debug(str(th.before))
    logger.debug("MATCH: " + str(th.after))
    sl(startdate)
    
    rtn = ex(['SPK object STOP'], timeout=dt)
    logger.debug(str(th.before))
    logger.debug("MATCH: " + str(th.after))
    sl(stopdate)
    
    # We're just single-body routine
    rtn = ex(['Add more objects to file'], timeout=dt)
    logger.debug(str(th.before))
    logger.debug("MATCH: " + str(th.after))
    sl('no')

    rtn = ex(['ftp.*\r\n'], timeout=dt)
    logger.debug(str(th.before))
    logger.debug("MATCH: " + str(th.after))
    # URL has to be stripped out of \r\n charactes and decoded to string
    FTPURL = th.after.strip().decode('utf-8')
    logger.info("FTP url: " + FTPURL)

    sl('quit')
    return FTPURL, OBJID


class SBSPK(object):
    ''' 
    Retrieves a small-body SPICE binary kernel from the JPL Horizons system.
    
    Kernel files are saved to disk. Horizons telnet interface is used.
    A telnet client has to be installed on your system, as well as your 
    firewall must allow for a telnet connection to horizons.jpl.nasa.gov
    on a port 6775, and for establishing a passive ftp conection.
    
    This class has a number of user-accesible parameters and a single 
    ``SBSPK.get`` method launching the kernel generation. Some human-readable
    retrieval status information is logged at the INFO level using the 
    standard Python ``logging`` module.
    
    Example usage:
    
    >>> import os
    >>> from sbspk import SBSPK
    >>> s = SBSPK()
    >>> s.get("2000 SG344", directory=os.getcwd())
    [('/tmp/3054374_2000_SG344.bsp', '3054374')]

    Interaction with Horizons is fragile and over the years can be broken
    even by minor changes in the telnet interface, thus was implemented 
    solely in a ``sbspk._sbspk.talk`` function.
    
    The SBSPK class ``__init__`` method takes ``_talkfunc`` keyword arg
    that defaults to ``sbspk._sbspk.talk`` function. Other functions 
    can be supplied here as a drop-in replacement if they match 
    ``sbspk._sbspk.talk`` args and returns.
    '''
    
    printprogress = False
    ''' Prints the SPK download progress meter. This is separate from 
    logging and turned off by default. '''
    
    email = 'sorry@noemail.org'     #: Email address required by Horizons SPK generation 
    """Email address required by Horizons SPK generation. """

    startdate = '2010-01-01'
    ''' Ephemeris start date for an SPK file, default is ``'2010-01-01'``. '''
    
    stopdate = '2040-01-01'
    ''' Ephemeris stop date for an SPK file, default is ``'2040-01-01'``. '''
    
    timeout = 5
    ''' Max time to wait for an expected JPL Horizons output (seconds).
    After this a ``pexpect.TIMEOUT`` exception will be thrown. '''
    
    fileformat = "<OBJID>_<TARGET>.bsp"
    ''' Kernel file name format. ``<OBJID>`` will be replaced with 
    a current object ID, ``<TARGET>`` will be replaced with a specified
    targe name. Be carefull - files will be overwritten without 
    any warning. '''
    
    def __init__(self, _talkfunc=talk):
        self.logger = logging.getLogger("SBSPK_Logger")
        # we assing it here, so its a function, not a bound method
        self._talk_to_horizon_func = _talkfunc
    
    def __print_download_progress(self, count, blockSize, totalSize):
        if self.printprogress:
            percent = min(int(count*blockSize*100/totalSize), 100)
            sys.stdout.write("\rDownloading kernel... %2d%%" % percent)
            sys.stdout.flush()
    
    def get(self, target, directory='/tmp'):
        ''' Generates and downloads ``target``-body binary SPK file.
        
        If Horizons system cannot find a given target object (or its 
        object ID cannot be parsed out of telnet output) an
        ``sbspk.SBSPKError`` exception will be thrown.
        
        Parameters:
            target: Solar System small body name to retrive. Can be 
                    either a single string or a list/tuple of strings,
                    for example:
                    
                    >>> s = SBSPK()
                    >>> s.get('2000 SG344')
                    [('/tmp/3054374_2000_SG344.bsp', '3054374')]
                    >>> s.get(['2014 SU1', '2015 TB'])
                    [('/tmp/3689273_2014_SU1.bsp', '3689273'), 
                     ('/tmp/3728897_2015_TB.bsp', '3728897')]

            directory: Directory to which kernel file(s) will be 
                       downloaded to. Defaults to ``'/tmp'``.
        Returns: 
            List of ``[SPK_file, horizons_object_ID]``, (str, str) pairs.
        
        TODO: smarter retrieving
        '''
        if isinstance(target, str):
            target = [target]
            
        paths_and_objids = []
        for trgt in target:
            r = self.__get_one(trgt, directory)
            paths_and_objids.append(r)
        return paths_and_objids
        
    def __get_one(self, target, directory):
        target = target.strip()
        self.logger.info("Retrieving " + target)
        try:
            url, objid = self._talk_to_horizon_func(target, self.email, 
                            self.startdate, self.stopdate, self.timeout)
        except pexpect.TIMEOUT:
            self.logger.error("TIMED OUT. Perhaps inteface changed?")
            raise
        else:
            filename = self.fileformat.replace("<OBJID>", objid).replace("<TARGET>", target.replace(' ', '_'))
            filepath = os.path.join(directory, filename)
            urlret = urlretrieve(url, filepath, reporthook=self.__print_download_progress)
            if self.printprogress: 
                print('  Done.')
            self.logger.info('Kernel file can be found at ' + urlret[0])
            return urlret[0], objid

