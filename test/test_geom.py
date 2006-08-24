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
