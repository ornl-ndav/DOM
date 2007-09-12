The DOM (Data Object Model) package is designed for reading raw data NeXus 
files and writing files from data reduction.

Authors: Michael Reuter <reuterma@ornl.gov>
	 Peter Peterson <petersonpf@ornl.gov

Installation Instructions
=========================

  Software Requirements
  ---------------------

  The DOM package requires the NeXus (http://www.nexusformat.org) libraries in 
  order to function properly. NeXus has its own set of dependencies 

  DOM currently works best under Linux, but has been occasionaly known to work 
  under OSX. The following lists the current versions of software that DOM has 
  been known to work under.

    1. NeXus Libraries - 4.0.0
       a. HDF5	       - 1.6.5
       b. MXML	       - 2.2.2
       c. HDF4	       - 4.2r1
    2. Python          - 2.3.4
    3. GCC	       - 3.4.6

  Installation
  ------------

  The DOM package follows standard Python installations:

  python setup.py install

  The default install location is /usr/local. To override this location, use 
  the --prefix option.

  The setup script expects the NeXus libraries and include files to be located 
  in /usr/local. To override this location, use the --with-nexus option and 
  provide the alternate location. The --with-nexus option can be used in 
  either of the following manners.

    1. --with-nexus=/path/to/install
    2. --with-nexus=/path/to/includes/include,/path/to/libs/lib


$Id$
