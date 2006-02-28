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
        print " SO IDS:",dst.get_SO_ids(item)
        
