import sns_napi
print dir(sns_napi)
#help(sns_napi)
handle=sns_napi.open("/home/pf9/DAS_2.nxs")
sns_napi.opengroup(handle,"entry","NXentry");
