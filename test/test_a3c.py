#!/usr/bin/env python

# $Id$

import dst_base
from so import SO
from som import SOM
from time import localtime, strftime, time

filename_SOM1 = "stuff1.dat"

SOM1 = SOM()
SOM1.attr_list["filename"] = filename_SOM1
SOM1.attr_list["epoch"] = time()
SOM1.attr_list["timestamp"] = strftime("%Y-%m-%d %T",
                                       localtime(SOM1.attr_list["epoch"]))

for i in range(2):
    SO1 = SO()
    for j in range(10):
        SO1.id = j
        SO1.x.append(j+1)
        SO1.y.append(1000+j+(20*j))
        SO1.var_y.append(100+j)

    SOM1.append(SO1)

file = open(filename_SOM1, "w")

a3c = dst_base.getInstance("text/Spec", file)
a3c.writeSOM(SOM1)
a3c.release_resource()


