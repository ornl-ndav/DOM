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

import sns_napi
import nessi_list
import timing
import time

def print_mark(tag,milli):
    sec=(milli-(milli%1000))/1000
    milli=milli-sec*1000
    print "%18s :%02d.%03d" % (tag,sec,milli)

def getdata(handle):
    data=sns_napi.getdata(handle)
    nessi_data=nessi_list.NessiList()
    nessi_data.__array__.__set_from_NessiVector__(nessi_data.__array__,data)
    return nessi_data

def getslab(handle,start,size):
    data=sns_napi.getslab(handle,start,size)
    nessi_data=nessi_list.NessiList()
    nessi_data.__array__.__set_from_NessiVector__(nessi_data.__array__,data)
    return nessi_data

print dir(sns_napi)
#help(sns_napi)
handle=sns_napi.open("/SNS/users/pf9/REF_M_50-zipped.nxs")
print "opengroup(entry,NXentry)",sns_napi.opengroup(handle,"entry","NXentry")
#print "opengroup(data,NXdata)",sns_napi.opengroup(handle,"data","NXdata")
print "opengroup(bank1,NXdata)",sns_napi.opengroup(handle,"bank1","NXdata")
print "getnextentry()",sns_napi.getnextentry(handle)
print "getnextentry()",sns_napi.getnextentry(handle)
print "opendata(x_pixel_offset)",sns_napi.opendata(handle,"x_pixel_offset")
print "getattr(axis)",sns_napi.getattr(handle,"axis")
print "getattr(units)",sns_napi.getattr(handle,"units")
xpo=sns_napi.getdata(handle)
print "getdata()",xpo.__type__,xpo,len(xpo)
print "closedata()",sns_napi.closedata(handle)
print "opendata(data)",sns_napi.opendata(handle,"data")
(dims,type)=sns_napi.getinfo(handle)
print "getinfo()",(dims,type)
print "getnextattr()",sns_napi.getnextattr(handle)
print "getdata benchmark [:sec.milli]"
timing.start()
sns_napi.getdata(handle)
timing.finish()
print_mark("",timing.milli())
print "getslab((0,0,0),(1,1,167))",sns_napi.getslab(handle,(0,0,0),(1,1,167))
print "getslab((1,1,0),(1,1,167))",sns_napi.getslab(handle,(1,0,0),(1,1,167))

