#!/usr/bin/env python
###############################################################################
#
# Script for installing the DOM package modules
#
# $Id$
#
###############################################################################

from distutils.core import setup, Extension
import os
import sys

# Package name and version information
PACKAGE = "DOM"
VERSION = "none"

# Minimum version of Python
PYTHON_MAJOR = 2
PYTHON_MINOR = 2

if sys.version_info < (PYTHON_MAJOR, PYTHON_MINOR):
        print >> sys.stderr, 'You need at least Python %d.%d for %s %s' \
                                      % (PYTHON_MAJOR, PYTHON_MINOR,
					 PACKAGE, VERSION)
	sys.exit(3)

nexus_incdir = '/usr/local/include'
incdir_list = [nexus_incdir]

nexus_libdir = '/usr/local/lib/'
libdir_list = [nexus_libdir]

nexus_lib = "NeXus"
lib_list_all = [nexus_lib]

if os.uname()[0] == 'Linux':
            lib_list_all.append('stdc++')
            
def main():
    setup(name=PACKAGE,
          version=VERSION,
          extra_path=PACKAGE,
          package_dir={"": "."},
          packages=["DST", "SOM"],
          ext_modules = [Extension( "sns_napi", ["nexus/sns_napi.cpp"] ,
                                    include_dirs = incdir_list,
                                    library_dirs = libdir_list,
                                    libraries = lib_list_all)],
          )

if __name__ == "__main__":
    main()
