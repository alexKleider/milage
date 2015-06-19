#!/usr/bin/env python

import sys
import os.path

def parse_line(l):
    try:
        list = l.split(',')
        odo = int(list[0])
        gal = float(list[1])
        return (odo, gal)
    except ValueError, e:
        return None

n_args = len(sys.argv)

if n_args==1:
    print """Usage:
    mileage.py file [odometer_reading]
You have not provided any argument(s.)"""
    sys.exit(1)

fname = sys.argv[1]
if not os.path.isfile(fname):
    print """Aborting program: "%s" is not a valid file."""%(fname, )
    sys.exit(1)

if n_args>2:
    prev = int(sys.argv[2])
else:
    prev = 0

count = sum = 0
fuel = 0.0

for line in open(fname):
    if line:
        try:
            odo, gal = parse_line(line)
            if prev!=0:
                miles = odo - prev
                sum = sum + miles
                fuel = fuel + gal
                count+=1
                milage = miles/gal
                print "%4d miles on %2.3f galons = %3f miles per gallon"%\
                                          (miles, gal, milage,)
            prev = odo
        except TypeError, e:
            print "Unparseable line: '%s'."%(line[:-1], )

milage = sum/fuel
print "SUMMARY: Average fuel consumption is %3.2f miles per gallon" %(milage,)

