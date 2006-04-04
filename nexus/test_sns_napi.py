import sns_napi
print dir(sns_napi)
#help(sns_napi)
handle=sns_napi.open("/home/pf9/DAS_2.nxs")
print "opengroup(entry,NXentry)",sns_napi.opengroup(handle,"entry","NXentry");
print "opengroup(data,NXdata)",sns_napi.opengroup(handle,"data","NXdata");
print "opendata(x_pixel_offset)",sns_napi.opendata(handle,"x_pixel_offset");
print "getattr(axis)",sns_napi.getattr(handle,"axis");
print "getattr(units)",sns_napi.getattr(handle,"units");
