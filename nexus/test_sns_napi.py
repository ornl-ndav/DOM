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
handle=sns_napi.open("/home/pf9/DAS_2.nxs")
print "opengroup(entry,NXentry)",sns_napi.opengroup(handle,"entry","NXentry")
print "opengroup(data,NXdata)",sns_napi.opengroup(handle,"data","NXdata")
print "getnextentry()",sns_napi.getnextentry(handle)
print "getnextentry()",sns_napi.getnextentry(handle)
print "opendata(x_pixel_offset)",sns_napi.opendata(handle,"x_pixel_offset")
print "getattr(axis)",sns_napi.getattr(handle,"axis")
print "getattr(units)",sns_napi.getattr(handle,"units")
print "getdata()",getdata(handle)
print "closedata()",sns_napi.closedata(handle)
print "opendata(data)",sns_napi.opendata(handle,"data")
(dims,type)=sns_napi.getinfo(handle)
print "getinfo()",(dims,type)
print "getnextattr()",sns_napi.getnextattr(handle)
print "getdata benchmark [:sec.milli]"
timing.start()
data=getdata(handle)
timing.finish()
print_mark("",timing.milli())
print "getslab((0,0,0),(0,0,167))",getslab(handle,(0,0,0),(0,0,167))
print "getslab((1,0,0),(1,0,167))",getslab(handle,(1,0,0),(1,0,167))

