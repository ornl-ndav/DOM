###############################################################################
#
# Script for installing the DOM package modules
#
# $Id$
#
###############################################################################

from distutils.core import setup

package_name = "DOM"
version_id = "none"

def main():
    setup(name=package_name,
          version=version_id,
          extra_path=package_name,
          package_dir={"": "."},
          packages=["DST", "SOM"])

if __name__ == "__main__":
    main()
