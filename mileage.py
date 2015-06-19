#!venv/bin/python3
# -*- coding: utf-8 -*-
# vim: set file encoding=utf-8 :
#
# file: 'mileage.py'
# Part of ___, ____.

# Copyright 2015 Alex Kleider
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#   Look for file named COPYING.
"""
mileage.py is a script that calculates gas mileage.

Usage:
mileage.py (-h | --version)
mileage.py INFILE [MILEAGE]

Options:
  -h --help  Prints this docstring.
  --version  Prints version number.
  INFILE  Input file.
  MILEAGE  Beginning mileage. If not provided, milage (but not
           fuel volume) of first entry will be used. (default: 0)
"""

# from __future__ imports
# import standard library modules
import sys
import os.path
# import custom modules
import docopt
# metadata such as version number
VERSION = "0.0.1"
# other constants
# global variables
# custom exception types
# private functions and classes
# public functions and classes
# main function
#

def parse_line(l):
    try:
        list = l.split(',')
        odo = int(list[0])
        gal = float(list[1])
        return (odo, gal)
    except ValueError:
        return None

def main():
    args = docopt.docopt(__doc__, version=VERSION)
#   print(args)
#   sys.exit()

    fname = args['INFILE']
    if not os.path.isfile(fname):
        print("""Aborting program: "{}" is not a valid file."""
                    .format(fname ))
        sys.exit(1)

    if args['MILEAGE']:
        try:
            prev = int(args['MILEAGE'])
        except ValueError:
            print("Invalid 'MILEAGE' argument.")
            print("Will ignore first fuel volume.")
            prev = 0
    else:
        prev = 0

    count = sum = 0
    fuel = 0.0

    with open(fname, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    odo, gal = parse_line(line)
                    if prev!=0:
                        miles = odo - prev
                        sum = sum + miles
                        fuel = fuel + gal
                        count+=1
                        milage = miles/gal
                        print(
        "{:.3f} miles on {:2.3f} galons = {:.3f} miles per gallon"
                                  .format(miles, gal, milage))
                    prev = odo
                except TypeError:
                    print("Unparseable line: '{}'."
                            .format(line))

    milage = sum/fuel
    print(
        "SUMMARY: Average fuel consumption is {:3.2f} miles per gallon"
                .format(milage))

if __name__ == '__main__':  # code block to run the application
    print("Running Python3 script: 'mileage.py'.......")
    main()
