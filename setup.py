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
VERSION = "1.0.0itc1"

# Package list
package_list = ['', 'DST', 'SOM']

def pythonVersionCheck():
    # Minimum version of Python
    PYTHON_MAJOR = 2
    PYTHON_MINOR = 2
    
    if sys.version_info < (PYTHON_MAJOR, PYTHON_MINOR):
            print >> sys.stderr, 'You need at least Python %d.%d for %s %s' \
                  % (PYTHON_MAJOR, PYTHON_MINOR, PACKAGE, VERSION)
            sys.exit(3)

            
def parseOptions( argv, keywords ):
    """get values for input keywords

    inputs like:
    --keyword=value

    transformed to a dictionary of 
    {keyword: value}

    if nothing is given, value is set to default: True
    """
    res = {}
    for keyword in keywords:
        for i, item in enumerate(argv):
            if item.startswith(keyword):
                value = item[ len(keyword) + 1: ]
                if value == "": value = True
                res[keyword] = value
                del argv[i]
                pass
            continue
        continue
    return res

def parseCommandLine():
    argv = sys.argv

    keywords = ['--with-nexus']
    options = parseOptions(argv, keywords)

    file_locations = None
    if options.get('--with-nexus'):
        file_locations = options['--with-nexus'].split(',')

    return file_locations


def setupSnsNapiExt(locations):

    if locations == None:
        nexus_incdir = '/usr/local/include'
        nexus_libdir = '/usr/local/lib'
    else:
        if len(locations) == 1:
            nexus_incdir = locations[0]+'/include'
            nexus_libdir = locations[0]+'/lib'
        else:
            nexus_incdir = locations[0]
            nexus_libdir = locations[1]
                    
    incdir_list = [nexus_incdir]
    libdir_list = [nexus_libdir]
    
    nexus_lib = "NeXus"
    lib_list_all = [nexus_lib]
    
    if os.uname()[0] == 'Linux':
        lib_list_all.append('stdc++')
            
    return [Extension("sns_napi",
                      [os.path.join('nexus', 'sns_napi.cpp')],
                      include_dirs = incdir_list,
                      library_dirs = libdir_list,
                      libraries = lib_list_all)]


if __name__ == "__main__":
    pythonVersionCheck()
    file_locations = parseCommandLine()
    sns_napi_ext = setupSnsNapiExt(file_locations)

    setup(name=PACKAGE,
          version=VERSION,
          extra_path=PACKAGE,
          packages=package_list,
          ext_modules=sns_napi_ext)

        

