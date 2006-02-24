###############################################################################
#
# Script for installing the DOM package modules
#
# $Id$
#
###############################################################################
#!/usr/bin/env python

from distutils.core import setup
import sys

# Package name and version information
PACKAGE = "DOM"
VERSION = "none"

# Minimum version of Python
PYTHON_MAJOR = 2
PYTHON_MINOR = 2

if sys.version_info < (PYTHON_MAJOR, PYTHON_MINOR):
        print >>sys.stderr, 'You need at least Python %d.%d for %s %s' \
                                      % (PYTHON_MAJOR, PYTHON_MINOR,
					 PACKAGE, VERSION)
	sys.exit(3)
            
def main():
    setup(name=PACKAGE,
          version=VERSION,
          extra_path=PACKAGE,
          package_dir={"": "."},
          packages=["DST", "SOM"])

if __name__ == "__main__":
    main()
