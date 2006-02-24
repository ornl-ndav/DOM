#!/usr/bin/env python

# $Id$

import ascii3col_dst
from so import SO
from som import SOM
from time import localtime, strftime, time

filename_SOM1 = "stuff1.dat"

SOM1 = SOM()
SOM1.attr_list["filename"] = filename_SOM1
SOM1.attr_list["epoch"] = time()
SOM1.attr_list["timestamp"] = strftime("%Y-%m-%d %T",
                                       localtime(SOM1.attr_list["epoch"]))
SOM1.attr_list["username"] = "Michael Reuter and the Gang"
SOM1.attr_list["x_units"] = "microseconds"
SOM1.attr_list["y_units"] = "beats"

for i in range(2):
    SO1 = SO()
    for j in range(10):
        SO1.id = i
        SO1.x.append(j+1)
        SO1.y.append(1000+j+(20*j))
        SO1.var_y.append(100+j)
    SO1.x.append(11)

    SOM1.append(SO1)

file = open(filename_SOM1, "w")

a3c = ascii3col_dst.Ascii3ColDST(file)
a3c.writeSOM(SOM1)
a3c.release_resource()


