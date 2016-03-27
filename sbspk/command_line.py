#!/usr/bin/env python3
""" ``sbspk`` package provides a simple command-line ``sbspk`` utility: """
import os
import sys
import logging
import argparse
from sbspk import SBSPK


def _get_argparser():
    ''' Function returning a pre-filled argument parser '''
    parser = argparse.ArgumentParser(description=("Retrieves small-body SPICE kernels from the command-line."
                        " Files are saved in current working directory."),
                        epilog='Example: sbspk -t "2000 SG344" "2014 SU1"')
    parser.add_argument('-v', dest='loglevel', help='verbose (DEBUG) mode', 
                        action='store_const', const=logging.DEBUG, default=logging.INFO)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-t', dest='targets', metavar='TARGET', type=str, 
                       nargs='+', help='specify one or many target names from the command line, spaces need to be quoted')
    group.add_argument('-f', dest='filename', help='read a text file with target names (one per line)')
    return parser


def main():
    parser = _get_argparser()
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)

    p = parser.parse_args()
    logging.basicConfig(level=p.loglevel, format='%(levelname)s - %(message)s')
    
    if p.targets is not None:
        targets = p.targets
    elif p.filename is not None:
        with open(p.filename, 'r') as f:
            targets = [t.strip() for t in f]
    else:
        raise RuntimeError

    a = SBSPK()
    a.printprogress = True
    a.get(targets, directory=os.getcwd())
