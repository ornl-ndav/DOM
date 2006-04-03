#!/usr/bin/python
import os
from distutils.core import setup, Extension

nexus_incdir = '/usr/local/include'
napi_incdir  = '.' 

nexus_libdir = '/usr/lib/'

incdir_list = [napi_incdir]
libdir_list = [nexus_libdir]

nexus_lib = "NeXus"

lib_list_all = [nexus_lib]


if os.uname()[0] == 'Linux':
    lib_list_all.append('stdc++')

setup( name = "nxpython",
       version = "0.1",
       description = "Nexus extension module for Python",
       author = "Hartmut Gilde",
       author_email = "hartmut.gilde@frm2.tum.de",
       url = "http://www.frm2.tum.de",
       ext_modules = [Extension( "_nexus", ["napi_swig.i"] ,
                                 include_dirs = incdir_list,
                                 library_dirs = libdir_list,
                                 libraries = lib_list_all)],
       ) 

setup( name = "nxpython",
       version = "0.1",
       description = "Nexus extension module for Python",
       author = "Hartmut Gilde",
       author_email = "hartmut.gilde@frm2.tum.de",
       url = "http://www.frm2.tum.de",
		 py_modules = ['nexus']
       ) 

