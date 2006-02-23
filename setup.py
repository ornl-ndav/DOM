###############################################################################
#
# Script for installing the DOM package modules
#
# $Id$
#
###############################################################################

from distutils.core import setup
import sys,os
import glob

package_name = "DOM"
#DOM_components = ['DST.ascii3col_dst', 'DST.dst_base',
#                  'DST.nexus_dst', 'SOM.attribute', 'SOM.so',
#                  'SOM.som']

# For when __init.py__ is available
DOM_components = ['DOM','DOM/DST', 'DOM/SOM']

setup(name=package_name,
      version='None',
      package_dir={'DOM': ''},
      #py_modules=DOM_components)
      packages=DOM_components)
