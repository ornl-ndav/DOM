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

import time as _time
from datetime import tzinfo, timedelta

ZERO = timedelta(0) 
"""Placeholder for zero I{seconds}"""

STDOFFSET = timedelta(seconds = -_time.timezone)
"""Time difference (I{seconds}) from UTC (no DST)"""
if _time.daylight:
    DSTOFFSET = timedelta(seconds = -_time.altzone)
    """Time difference (I{seconds}) from UTC, value depending on DST"""
else:
    DSTOFFSET = STDOFFSET

DSTDIFF = DSTOFFSET - STDOFFSET
"""Time shift (I{seconds}) for DST in local time zone"""

class LocalTimezone(tzinfo):
    """
    This class is a concrete implementation of the C{tzinfo} abstract base
    class. It handles information dealing with daylight savings issues.
    """
    
    def utcoffset(self, dt):
        """
        This method determines the time offset (I{seconds}) from UTC for the
        local time zone. This method takes into account if the local time
        zone is in Daylight Savings Time (DST). The returned value is negative
        is the local time zone is west of UTC and positive if east of UTC.

        @param dt: The object containing date/time information
        @type dt: C{datetime}


        @return: The time offest from UTC
        @rtype: C{int}
        """
        if self._isdst(dt):
            return DSTOFFSET
        else:
            return STDOFFSET

    def dst(self, dt):
        """
        This method returns the time shift (I{seconds}) for Daylight Savings
        Time in the local time zone. If the local time zone is not in DST, this
        value is 0.

        @param dt: The object containing date/time information
        @type dt: C{datetime}


        @return: The current time shift for Daylight Savings Time
        @rtype: C{int}
        """
        if self._isdst(dt):
            return DSTDIFF
        else:
            return ZERO

    def tzname(self, dt):
        """
        This method retrieves the name of the local time zone taking into
        consideration Daylight Savings Time.
        
        @param dt: The object containing date/time information
        @type dt: C{datetime}


        @return: The string representation of the local time zone
        @rtype: C{string}
        """
        return _time.tzname[self._isdst(dt)]

    def _isdst(self, dt):
        """
        This private method checks to see if the local time zone is in Daylight
        Savings Time. 

        @param dt: The object containing date/time information
        @type dt: C{datetime}


        @return: True if the local time zone is in DST and False if it is not
        @rtype: C{boolean}
        """
        tt = (dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second,
              dt.weekday(), 0, -1)
        stamp = _time.mktime(tt)
        tt = _time.localtime(stamp)
        return tt.tm_isdst > 0
