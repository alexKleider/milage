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
mileage.py [-c] INFILE [MILEAGE]

Options:
  -h --help  Prints this docstring.
  --version  Prints version number.
  -c --include_comments  Includes the comments in the output
  INFILE  Input file.
  MILEAGE  Beginning mileage. If not provided, mileage (but not
           fuel volume) of first entry will be used. (default: 0)

Each line of INFILE is expected to be in the following format:
mileage, gallons
eg:
47333, 15.580

A line in the following format is acceptable:
mileage, gallons, <anything you want>
eg:
47333, 15.580, August 4 Elko Nevada, cheapest grade @ 3.25, $48.24
Anything after the second comma is an optional comment.

Any line that can not be parsed, is reported as such and ignored.

"""

# from __future__ imports
# import standard library modules
import sys
import os.path
# import custom modules
import docopt
# metadata such as version number
VERSION = "0.0.2"
# other constants
# global variables
# custom exception types
# private functions and classes
# public functions and classes
# main function
#


KLICKS_IN_A_MILE = 1.62
LITRES_PER_GALLON = 3.8  # US Gallon
    # Imperial Gallon is more by 4/3.


def convert_as_needed(source, sentinal=(), factor=1):
    """
    Helper function: 
        checks if last character of <source> (a string)
        is in <sentinal> (a tuple of one character strings)
        if so: returns float(source[:-1]) * factor
        else: returns float(source)
        Returns False if parsing fails.
    """
    convert = False
    try:
        last_character = source[-1]
    except IndexError:
        return

    if last_character in sentinal:
        source = source[:-1]
        convert = True
    try:
        ret = float(source)
    except ValueError:
        return
    if convert:
        return ret * factor
    else:
        return ret

def parse_line(l):
    """
    Attempts to extract a tuple of three items from the line which is
    assumed to be in CSV format.
    The first two will be floats, and the last a (possibly empty)
    string.
    If parsing is unsuccessful, returns None.
    The first item is the odometer reading and if ending in a 'K' or a
    'k', it will be assumed to be in kilometers and will be converted
    to miles.
    Similarly the second item is assumed to be in (US) gallons but if
    ending in a 'L' or a 'l', will be converted from litres to
    gallons.
    """
    list = l.split(',')
    if len(list) < 2:
        return
    odo = convert_as_needed(list[0], ('K', 'k'),
        1/KLICKS_IN_A_MILE )
    volume = convert_as_needed(list[1], ('L', 'l'),
        1/LITRES_PER_GALLON)
    if odo and volume:
        comment = ','.join(list[2:])
        return (odo, volume, comment)
    else:
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

    #set prev and adjust if required:
    prev = 0.0
    if args['MILEAGE']:
        try:
            prev = float(args['MILEAGE'])
        except ValueError:
            print("Invalid 'MILEAGE' argument.")
            print("Will ignore first fuel volume.")
            prev = 0.0

    count = 0
    total_miles = fuel = 0.0

    with open(fname, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    odo, gal, comment = parse_line(line)
                    if prev!=0:
                        miles = odo - prev
                        total_miles = total_miles + miles
                        fuel = fuel + gal
                        count+=1
                        milage = miles/gal
                        print(
        "{:.1f} miles on {:2.3f} galons = {:.3f} miles per gallon"
                                  .format(miles, gal, milage))
                        if args["--include_comments"] and comment:
                            print("\t{}".format(comment))
                    prev = odo
                except TypeError:
                    print("Unparseable line: '{}'."
                            .format(line))

    milage = total_miles/fuel
    print( "SUMMARY:")
    print(
    "Avg fuel consumption (over {:.1f} mi.) is {:3.2f} mpg."
                .format(total_miles, milage))

if __name__ == '__main__':  # code block to run the application
    print("Running Python3 script: 'mileage.py'.......")
    main()
