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
import hlr_utils
import SOM
import sys

if __name__ == "__main__":
    filename = None
    try:
        filename = sys.argv[1]
    except IndexError:
        pass # use the default name

    dst = DST.getInstance("application/x-NeXus", filename)
    som = dst.getSOM(("/entry/bank1", 1))

    # Write out file
    ofile = open("test.par", "w")
    par = DST.ParDST(ofile)
    par.writeSOM(som)
    par.release_resource()
