#!/usr/bin/env python

# $Id$

import DST
from SOM import SOM
import hlr_utils

filename = "test.xml"

SOM = SOM()
conf = hlr_utils.Configure()
conf.verbose = True
SOM.attr_list["config"] = conf

ofile = open(filename, "w")

mdw = DST.MdwDST(ofile)
mdw.writeSOM(SOM)
mdw.release_resource()
