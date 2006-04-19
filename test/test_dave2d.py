#!/usr/bin/env python

# $Id$

import DST
from SOM import SOM
from SOM import SO
from time import localtime, strftime, time

filename_SOM1 = "stuff1.dat"

SOM1 = SOM()
SOM1.attr_list["filename"] = filename_SOM1
SOM1.attr_list["epoch"] = time()
SOM1.attr_list["timestamp"] = DST.make_ISO8601(SOM1.attr_list["epoch"])
SOM1.attr_list["username"] = "Michael Reuter and the Gang"
SOM1.setAllAxisLabels(["Q", "E"])
SOM1.setAllAxisUnits(["A-1", "meV"])
SOM1.setYLabel("Intensity")
SOM1.setYUnits("Counts/(meV A-1))")

SO1 = SO(2)
SO1.id = 0
SO1.axis[0].val.extend(range(5))
SO1.axis[1].val.extend(range(10))

y_len = (len(SO1.axis[0].val)-1) * (len(SO1.axis[1].val)-1)
y = range(y_len)
SO1.y.extend(y)
SO1.var_y.extend(y)

SOM1.append(SO1)

file = open(filename_SOM1, "w")

d2d = DST.Dave2dDST(file)
d2d.writeSOM(SOM1)
d2d.release_resource()
