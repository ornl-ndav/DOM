#                        Data Object Model
#           A part of the SNS Analysis Software Suite.
#
#                  Spallation Neutron Source
#          Oak Ridge National Laboratory, Oak Ridge TN.
#
#
#                             NOTICE
#
# For this software and its associated documentation, permission is granted
# to reproduce, prepare derivative works, and distribute copies to the public
# for any purpose and without fee.
#
# This material was prepared as an account of work sponsored by an agency of
# the United States Government.  Neither the United States Government nor the
# United States Department of Energy, nor any of their employees, makes any
# warranty, express or implied, or assumes any legal liability or
# responsibility for the accuracy, completeness, or usefulness of any
# information, apparatus, product, or process disclosed, or represents that
# its use would not infringe privately owned rights.
#

# $Id$

import SOM

def make_ISO8601(now=None):
    """
    This function takes an optional argument of a UNIX time and converts that
    time to an U{ISO-8601<http://www.w3.org/TR/NOTE-datetime>} standard time
    string. If no UNIX time is given, the default is to use the current time.

    @param now: (OPTIONAL) A UNIX time (number of seconds after Jan 1, 1970)
    @type now: C{int}
    

    @returns: A time string in ISO-8601 standard format
    @rtype: C{string}
    """
    import datetime
    import ltz
    Local = ltz.LocalTimezone()

    if now is not None:
        return datetime.datetime(2006,1,1).fromtimestamp(now,Local).isoformat()
    else:
        return datetime.datetime(2006,1,1).now(Local).isoformat()

def make_magic_key():
    """
    This function creates a unique key for SNS created files.

    @returns: A unique key
    @rtype: C{int}
    """
    import random
    import time

    key = str(time.time())
    key = key.split('.')[0]+key.split('.')[1]

    adders = random.randint(1,10)

    counter = 0
    while counter < adders:
        len_s = len(key)
        ins = random.randint(0,len_s)
        val = random.randint(0,9)
        key = key[0:ins]+str(val)+key[ins:]
        counter += 1
    
    return key

def parse_spec_header(ifile):
    """
    This function reads through a Spec file parsing the header (or footer
    in the case of Dave2d) information and creating a dictionary from that
    information.

    @param ifile: The input file resource containing the Spec header
    @type ifile: C{file}


    @return: The gathered information from the Spec header
    @rtype: C{dict}
    """
    import os
    
    SPEC_HEADER_FLAGS = ["#F", "#C", "#E", "#D"]

    header_lines = {}
    for line in ifile:
        key = line[:2]
        if key in SPEC_HEADER_FLAGS:
            __update_dictionary(header_lines, key,
                                line.lstrip(key).rstrip(os.linesep), "lstr")
        else:
            break

    DATASET_TYPES = ["data", "normalization", "norm", "dsbackground",
                     "background", "empty_can"]

    DR_PACKAGES = ["HLR", "DOM", "SCL"]
    
    HEADER_KEYS = {
        "Title": ["title", "str"],
        "Notes": ["notes", "str"],
        "Run Number": ["run_number", "str"],
        "dt/t": ["dt_over_t", "nxpar"],
        "User": ["username", "str"],
        "Polar Angle Offset": ["angle_offset", "nxpar"],
        "Proton Charge": ["proton_charge", "nxpar"],
        "Slit1 Size": ["slit1_size", "nxpar"],
        "Slit2 Size": ["slit2_size", "nxpar"],
        "Slit3 Size": ["slit3_size", "nxpar"],
        "Slit1-Slit2 Distance": ["slit12_distance", "nxpar"],
        "Slit1-Slit3 Distance": ["slit13_distance", "nxpar"],
        "theta": ["theta", "nxpar"],
        "dtheta": ["delta_theta", "nxpar"],
        "dtheta_over_theta": ["dtheta_over_theta", "nxpar"],
        }

    attr_list = SOM.AttributeList()

    # Parse the files
    for file_line in header_lines[SPEC_HEADER_FLAGS[0]]:
        if ":" in file_line:
            parts = file_line.split(':')
            key = parts[0].strip() + "-filename"
            __update_dictionary(attr_list, key, parts[1], "lstr")
        else:
            __update_dictionary(attr_list, "filename", file_line, "lstr")

    # Parse the comments for information
    try:
        for comment_line in header_lines[SPEC_HEADER_FLAGS[1]]:
            parts = comment_line.split(':')

            if parts[0][:3] in DR_PACKAGES:
                continue

            found_data_set = [False, None]
            for data_set in DATASET_TYPES:
                if data_set in parts[0]:
                    found_data_set[0] = True
                    found_data_set[1] = data_set
                    break

            if found_data_set[0]:
                pkey = parts[0].lstrip(found_data_set[1]).strip()
                akey = found_data_set[1] + "-" + HEADER_KEYS[pkey][0]
                __update_dictionary(attr_list, akey, parts[1],
                                    HEADER_KEYS[pkey][1])
            else:
                pkey = parts[0].strip()
                try:
                    __update_dictionary(attr_list, HEADER_KEYS[pkey][0],
                                        parts[1], HEADER_KEYS[pkey][1])
                except KeyError:
                    # We've encountered something we don't know, write the info
                    # in as is
                    nkey = pkey.lower().replace(' ', '-')
                    __update_dictionary(attr_list, nkey, parts[1], "str")
    except KeyError:
        # No comment lines present, do nothing
        pass
    
    return attr_list

def units_from_string(ustr):
    """
    This function returns the units from a string of the form C{(units)}.

    @param ustr: The object to retrieve the units from
    @type ustr: C{string}


    @return: The units
    @rtype: C{string}
    """
    return ustr.lstrip('(').rstrip(')')

def __update_dictionary(idict, key, info, itype):
    """
    This private function updates a given dictionary with the information
    provided. The information is adjusted according to the type given.

    @param idict: The dictionary to be modified
    @type idict: C{dict}

    @param key: The key for the information
    @type key: C{string}

    @param info: The information to update the dictionary with
    @type info: C{string}

    @param itype: The data type for information conversion
    @type itype: C{string}
    """
    item = info.strip()

    if itype == "nxpar":
        item = SOM.NxParameter.fromString(item)

    if itype == "lstr":
        try:
            idict[key].append(item)
        except KeyError:
            idict[key] = [item]
    else:
        idict[key] = item
    
def write_spec_header(ofile, epoch, som):
    """
    This function writes a header based on the Spec file format.
    U{http://www.certif.com/spec_manual/user_1_4_1.html}

    @param ofile: The handle to the output file
    @type ofile: C{file}
    
    @param epoch: The UNIX time at creation
    @type epoch: C{float}
    
    @param som: The associated data
    @type som: L{SOM.SOM}
    """
    write_dataset_tags(ofile, "-filename", "#F %s: %s", "#F", som)

    print >> ofile, "#E", epoch
    print >> ofile, "#D", make_ISO8601(epoch)

    write_dataset_tags(ofile, "-run_number", "#C %s Run Number: %s",
                       "#C Run Number:", som)

    write_dataset_tags(ofile, "-title", "#C %s Title: %s", "#C Title:", som)

    write_dataset_tags(ofile, "-notes", "#C %s Notes: %s", "#C Notes:", som)  

    write_dataset_tags(ofile, "-dt_over_t", "#C %s dt/t: %f", "#C dt/t: %f",
                       som)
    
    if som.attr_list.has_key("username"):
        print >> ofile, "#C User:",som.attr_list["username"]
    else:
        pass
    
    if som.attr_list.has_key("angle_offset"):
        print >> ofile, "#C Polar Angle Offset:",\
              som.attr_list["angle_offset"]
    else:
        pass
    
    write_dataset_tags(ofile, "-proton_charge", "#C %s Proton Charge: %s",
                       "#C Proton Charge:", som)

    write_dataset_tags(ofile, "-slit1_size", "#C %s Slit1 Size: %s",
                       "#C Slit1 Size:", som)

    write_dataset_tags(ofile, "-slit2_size", "#C %s Slit2 Size: %s",
                       "#C Slit2 Size:", som)

    write_dataset_tags(ofile, "-slit3_size", "#C %s Slit3 Size: %s",
                       "#C Slit3 Size:", som)    

    write_dataset_tags(ofile, "-slit12_distance",
                       "#C %s Slit1-Slit2 Distance: %s",
                       "#C Slit1-Slit2 Distance:", som)

    write_dataset_tags(ofile, "-slit13_distance",
                       "#C %s Slit1-Slit3 Distance: %s",
                       "#C Slit1-Slit3 Distance:", som)    

    write_dataset_tags(ofile, "-delta_theta", "#C %s dtheta: %s",
                       "#C dtheta: %d", som)

    write_dataset_tags(ofile, "-theta", "#C %s theta: %s", "#C theta: %d", som)

    write_dataset_tags(ofile, "-dtheta_over_theta",
                       "#C %s dtheta_over_theta: %.10f",
                       "#C dtheta_over_theta: %.10f", som)
    
    # Write out software version numbers
    import common_lib
    import DST
    import utils

    # HLR
    print >> ofile, "#C HLR Version -", common_lib.__version__

    # DOM
    print >> ofile, "#C DOM Version -", DST.__version__

    # SCL
    print >> ofile, "#C SCL Version -", utils.__version__    
    
def write_dataset_tags(ofile, tag, format_multi, format_one, som):
    """
    This function searches a L{SOM.SOM} for a particular tag that has dataset
    dependent instances and writes that information to a file with the given
    formatting string.

    @param ofile: The handle to an output file.
    @type ofile: C{file}

    @param tag: The name of the tag holding the desired information. This
                includes the - but not the dataset tag.
    @type tag: C{string}

    @param format_multi: The desired formatting definition for the dataset
                         dependent information.
    @type format_multi: C{string}

    @param format_one: The desired formatting definition if the information is
                       not dataset dependent.
    @type format_one: C{string}    

    @param som: The object containing the information for search and retreival.
    @type som: L{SOM.SOM}
    """
    info_keys = [key for key in som.attr_list if key.find(tag) != -1]

    if len(info_keys):
        for info_key in info_keys:
            tag = info_key.split('-')[0]
            try:
                som.attr_list[info_key].reverse()
                som.attr_list[info_key].reverse()
                for info in som.attr_list[info_key]:
                    print >> ofile, format_multi % (tag, info)
            except AttributeError:
                print >> ofile, format_multi % (tag, som.attr_list[info_key])
    else:
        tag = tag.lstrip('-')
        if som.attr_list.has_key(tag):
            print >> ofile, format_one, som.attr_list[tag]

    
