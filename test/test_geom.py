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

#!/usr/bin/env python
import DST
import sys

if __name__=="__main__":
    data_filename = None
    geom_filename = None
    
    try:
        data_filename = sys.argv[1]
    except IndexError:
        pass # use the default name

    try:
        geom_filename = sys.argv[2]
    except IndexError:
        pass # use the default name

    id_tag = -1
    
    x_axis = "time_of_flight"
    dst = DST.getInstance("application/x-NeXus", data_filename)
    print "**********",data_filename
    som_list = dst.get_SOM_ids()
    print "SOM ID:",som_list[id_tag]

    som = dst.getSOM(som_list[id_tag], x_axis, end_id=(0,20))

    geom = DST.getInstance("application/x-NxsGeom", geom_filename)
    geom.setGeometry(som_list[id_tag], som)
