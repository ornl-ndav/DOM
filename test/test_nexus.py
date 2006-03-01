#!/usr/bin/env python
import dst_base
import sys

if __name__=="__main__":
    filename=None
    try:
        filename=sys.argv[1]
    except IndexError:
        pass # use the default name
    
    dst=dst_base.getInstance("application/x-NeXus",filename)
    print "**********",filename
    som_list=dst.get_SOM_ids()
    for item in som_list:
        print "FOR SOM:",item
        so_list=dst.get_SO_ids(item)
        print " SO IDS:",so_list
        so=dst.getSO(item,so_list[0])
        print " SO:",so_list[0]
        print "   id ",so.id
        print "   x  ",so.x
        print "   y  ",so.y
        print "   var",so.var_y
