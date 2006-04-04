import sns_napi
print dir(sns_napi)
#help(sns_napi)
file=sns_napi.NeXusFile("/home/pf9/DAS_2.nxs")
file.opengroup("entry","NXentry");
print file.filename,dir(file)
