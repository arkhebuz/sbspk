#!/usr/bin/env python3
""" SBSPK command line utility. """
import os
import sys
import logging
import argparse
from sbspk import SBSPK


def main():
    parser = argparse.ArgumentParser(description="sbspk")
    parser.add_argument('-v', dest='loglevel', help='verbose DEBUG mode', 
                        action='store_const', const=logging.DEBUG, default=logging.INFO)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-t', dest='targets', metavar='TARGET', type=str, 
                       nargs='+', help='one or many target names')
    group.add_argument('-f', dest='filename', help='file with target names')

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
