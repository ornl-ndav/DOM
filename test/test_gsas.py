#!/usr/bin/env python

# $Id$

import DST
from SOM import SOM
from SOM import SO

filename_SOM1 = "stuff1.dat"

SOM1 = SOM()
SOM1.attr_list["filename"] = filename_SOM1
SOM1.setTitle("This is a test")

for i in range(2):
    SO1 = SO()
    for j in range(10):
        SO1.id = i
        SO1.axis[0].val.append(j+1)
        SO1.y.append(1000+j+(20*j))
        SO1.var_y.append(100+j)
    SO1.axis[0].val.append(11)

    SOM1.append(SO1)

file = open(filename_SOM1, "w")

gsas = DST.GsasDST(file)
gsas.writeSOM(SOM1)
gsas.release_resource()


