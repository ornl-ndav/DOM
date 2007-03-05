#                        Data Object Model
#           A part of the SNS Analysis Software Suite.
#
#                  Spallation Neutron Source
#          Oak Ridge National Laboratory, Oak Ridge TN.
#
#
#                             NOTICE
#
# For this software and its associated documentation, permission is granted
# to reproduce, prepare derivative works, and distribute copies to the public
# for any purpose and without fee.
#
# This material was prepared as an account of work sponsored by an agency of
# the United States Government.  Neither the United States Government nor the
# United States Department of Energy, nor any of their employees, makes any
# warranty, express or implied, or assumes any legal liability or
# responsibility for the accuracy, completeness, or usefulness of any
# information, apparatus, product, or process disclosed, or represents that
# its use would not infringe privately owned rights.
#

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


