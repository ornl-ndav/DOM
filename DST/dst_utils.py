def make_ISO8601(now=None):
    """
    This function takes an optional argument of a UNIX time and converts that
    time to an ISO-8601 standard time string. If no UNIX time is given, the
    default is to use the current time.

    Parameters:
    ----------
    -> now (OPTIONAL) is a UNIX time (number of seconds after Jan 1, 1970)

    Returns:
    -------
    <- a time string in ISO-8601 standard format
    """
    
    import datetime
    import ltz
    Local = ltz.LocalTimezone()

    if now != None:
        return datetime.datetime(2006,1,1).fromtimestamp(now,Local).isoformat()
    else:
        return datetime.datetime(2006,1,1).now(Local).isoformat()


def make_magic_key():
    """
    This function creates a unique key for SNS created files.

    Returns:
    -------
    <- a unique key
    """

    import random
    import time

    key = str(time.time())
    key = key.split('.')[0]+key.split('.')[1]

    adders = random.randint(1,10)

    for i in range(adders):
        len_s = len(key)
        ins = random.randint(0,len_s)
        val = random.randint(0,9)
        key = key[0:ins]+str(val)+key[ins:]
    
    return key
