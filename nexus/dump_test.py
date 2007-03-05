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

# $Id$

#!/usr/bin/env python

import sns_napi
import nessi_list

axis_length=167
line_length=10

def file_exists(filename):
    import os.path
    return os.path.isfile(filename)

def print_help():
    print "usage: %s <filename>" % sys.argv[0]

def outname(inname):
    try:
        start=inname.rindex("/")+1
    except ValueError:
        start=0
    return inname[start:-3]+"dump"

def writeline(handle,data,index,line_end):
    stop=line_end-index
    if stop>line_length:
        stop=line_length
    for i in range(index,index+stop):
        handle.write("%d " % data[i])
    handle.write("\n")

def writeaxis(handle,data,index):
    start=index
    stop=index+axis_length
    while start<stop:
        writeline(handle,data,start,stop)
        start+=line_length

def writefile(handle,data,datasize):
    handle.write("File : %s, DataSet: data \n" % infile)
    handle.write(" %d  %d  %d \n" % (dims[0],dims[1],dims[2]))
    index=0
    while index<datasize:
        writeaxis(handle,data,index)
        index+=axis_length

def getdata(handle,dims,use_slabs=False):
    if not use_slabs:
        data=nessi_list.NessiList(type="double")
        return sns_napi.getdata(handle,data)

    data=nessi_list.NessiList(type="double")
    for x in range(dims[0]):
        for y in range(dims[1]):
            slab=nessi_list.NessiList(type="double")
            start=(x,y,0)
            stop=(1,1,dims[2])#x,y,dims[2])
            print start,stop,
            slab=sns_napi.getslab(handle,start,stop)
            print slab
            data.extend(slab)
    print len(data),data
    return data
    

if __name__=="__main__":
    # deal with the command line
    import sys
    try:
        infile=sys.argv[1]
    except IndexError:
        print_help()
        sys.exit(-1)
    if not file_exists(infile):
        print "File [%s] does not exist" % infile
        print_help()
        sys.exit(-1)
    outfile=outname(infile)

    # get to the data object
    inhandle=sns_napi.open(infile)
    sns_napi.opengroup(inhandle,"entry","NXentry")
    sns_napi.opengroup(inhandle,"data","NXdata")
    sns_napi.opendata(inhandle,"data")
    (dims,nxclass)=sns_napi.getinfo(inhandle)
    print "DIMS = ",dims
    print "TYPE = ",nxclass
    data=getdata(inhandle,dims,False)
    axis_length=dims[2]
    data_size=1
    for item in dims:
        data_size*=item
    print "SIZE:",len(data),data_size

    # print the data to a file
    print "writing to",outfile
    outhandle=open(outfile,mode="w")
    writefile(outhandle,data,data_size)
    outhandle.close()
