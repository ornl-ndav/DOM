#!/usr/bin/env python
import dst_base
import sys

if __name__=="__main__":
    filename="blah"
    try:
        filename=sys.argv[1]
    except IndexError:
        pass # use the default name
    
    
    dst=dst_base.getInstance("application/x-NeXus",filename)
    print dst
    
