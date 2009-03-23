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

    if "ARCS" in filename:
        cgeom = "/SNS/ARCS/2009_2_18_CAL/calibrations/ARCS_cgeom_20090128.txt"
    elif "CNCS" in filename:
        cgeom="/SNS/CNCS/2009_2_5_CAL/calibrations/CNCS_cgeom_20090224.txt"
    elif "SEQ" in filename or "SEQUOIA" in filename:
        cgeom="/SNS/SEQ/2009_2_17_CAL/calibrations/SEQ_cgeom_20090302.txt"
    else:
        raise RuntimeError("Cannot get corner geometry file")

    # Get corner geometry
    infile = open(hlr_utils.fix_filename(cgeom), "r")

    angle_info = {}
    counter = 0
    nexus_id = None
    angle_obj = None
    for line in infile:
        if line.startswith("b"):
            nexus_id = SOM.NeXusId.fromString(line.rstrip()).toTuple()
            counter = 0
            angle_obj = hlr_utils.Angles()
        else:
            angle_list = line.rstrip().split(' ')
            angles = [float(angle) for angle in angle_list]
            if counter == 1:
                angle_obj.setPolar(angles)
            else:
                angle_obj.setAzimuthal(angles)

        if counter == 2:
            angle_info[str(nexus_id)] = angle_obj

        counter += 1

    som.attr_list["corner_geom"] = angle_info

    # Write out file
    ofile = open("test.phx", "w")
    phx = DST.PhxDST(ofile)
    phx.writeSOM(som)
    phx.release_resource()
