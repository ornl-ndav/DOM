#!/usr/bin/env python

#                        Data Object Model
#           A part of the SNS Analysis Software Suite.
#
#                  Spallation Neutron Source
#          Oak Ridge National Laboratory, Oak Ridge TN.
#
#
#                             NOTICE
#
# For this software and its associated documentation, permission is granted
# to reproduce, prepare derivative works, and distribute copies to the public
# for any purpose and without fee.
#
# This material was prepared as an account of work sponsored by an agency of
# the United States Government.  Neither the United States Government nor the
# United States Department of Energy, nor any of their employees, makes any
# warranty, express or implied, or assumes any legal liability or
# responsibility for the accuracy, completeness, or usefulness of any
# information, apparatus, product, or process disclosed, or represents that
# its use would not infringe privately owned rights.
#

# $Id$

import sys
import DST

filename = sys.argv[1]

ifile = open(filename, "r")

a3c = DST.Ascii3ColDST(ifile)

som = a3c.getSOM()

a3c.release_resource()
index = 79
print "Length:", len(som)
print som.attr_list
print "Y Label:", som.getYLabel()
print "Y Units:", som.getYUnits()
print "X Labels:", som.getAllAxisLabels()
print "X Units:", som.getAllAxisUnits()
print som
print "Data:", som[0].axis[0].val[index], som[0].y[index], som[0].var_y[index]
