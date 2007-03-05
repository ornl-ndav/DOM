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

import DST
import sys

if __name__=="__main__":
    filename=None
    try:
        filename=sys.argv[1]
    except IndexError:
        pass # use the default name
    
    x_axis="time_of_flight"
    dst=DST.getInstance("application/x-NeXus",filename)
    print "**********",filename
    som_list=dst.get_SOM_ids()
    for item in som_list:
        print "FOR SOM:",item
        so_list=dst.get_SO_ids(item,x_axis)
#        print " SO IDS:",so_list
        so=dst.getSO(item,so_list[0],x_axis)
        print " SO:",so_list[0]
        print "   id ",so.id
        print "   x  ",so.axis[0].val
        print "   y  ",so.y
        print "   var",so.var_y
    som=dst.getSOM(som_list[0],x_axis,end_id=(0,20))
#    print som
    print som.attr_list
