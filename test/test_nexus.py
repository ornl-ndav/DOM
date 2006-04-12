#!/usr/bin/env python
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
