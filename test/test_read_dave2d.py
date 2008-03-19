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

d2d = DST.Dave2dDST(ifile)

som = d2d.getSOM()

d2d.release_resource()
x_index = 1
y_index = 31
N_y = len(som[0].axis[1].val)
print "N_y:", N_y
channel = y_index + (x_index * N_y)
print "channel:", channel
print som.attr_list
print "Y Label:", som.getYLabel()
print "Y Units:", som.getYUnits()
print "X Labels:", som.getAllAxisLabels()
print "X Units:", som.getAllAxisUnits()
print som
print "Data:", som[0].axis[0].val[x_index], som[0].axis[1].val[y_index], \
      som[0].y[channel], som[0].var_y[channel]
