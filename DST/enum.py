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

class Enum:
    """
    Create an enumerated type and then add var/value pairs to it. This was
    taken from U{http://www.norvig.com/python-iaq.html}.
    The constructor and the method .ints(names) take a list of variable names,
    and assign them consecutive integers as values.    The method .strs(names)
    assigns each variable name to itself (that is variable 'v' has value 'v').
    The method .vals(a=99, b=200) allows you to assign any value to variables.
    A 'list of variable names' can also be a string, which will be .split().
    The method .end() returns one more than the maximum int value.
    Example:

    >>> opcodes = Enum(\"add sub load store\").vals(illegal=255).
    """
  
    def __init__(self, names=[]):
        """
        Object constructor

        @param names:
        @type names: C{list} of C{string}s
        """
        self.ints(names)

    def set(self, var, val):
        """
        Set var to the value val in the enum.

        @param var: The name to give the value
        @type var: C{string}

        @param val: The value to associate with the name
        @type val: C{int}


        @return: A dictionary of key names and values
        @rtype: C{dict}
        """
        if var in vars(self).keys():
            raise AttributeError("duplicate var in enum")
        
        if val in vars(self).values():
            raise ValueError("duplicate value in enum")
        
        vars(self)[var] = val
        return self
  
    def strs(self, names):
        """
        Set each of the names to itself (as a string) in the enum.

        @param names: The key and value names for the enum
        @type names: C{string} or C{list} of C{string}s


        @return: A dictionary of key names and equivalent value names
        @rtype: C{dict}        
        """
        for var in self._parse(names):
            self.set(var, var)
        return self

    def ints(self, names):
        """
        Set each of the names to the next highest int in the enum.

        @param names: The key names for the enum
        @type names: C{string} or C{list} of C{string}s


        @return: A dictionary of key names and equivalent integer values
        @rtype: C{dict}
        """
        for var in self._parse(names):
            self.set(var, self.end())
        return self

    def vals(self, **entries):
        """
        Set each of var=val pairs in the enum.

        @param entries: A set of key-value pairs to assign
        @type entries: C{dict}


        @return: A dictionary of key names and equivalent integer values
        @rtype: C{dict}
        """
        for (var, val) in entries.items():
            self.set(var, val)
        return self

    def end(self):
        """
        One more than the largest int value in the enum, or 0 if none.

        @return: The largest value in the enum + 1
        @rtype: C{int}
        """
        try:
            return max([x for x in vars(self).values() \
                        if type(x) == type(0)]) + 1
        except ValueError:
            return 0
    
    def key(self, value):
        """
        This method returns the key for a given value.

        @param value: The value to key search
        @type value: C{int}


        @return: The key associated with the given value
        @rtype: C{string}


        @exception KeyError: Is raised if the requested value does not exist
                             within the enum.
        """
        vals = vars(self).values()
        try:
            index = vals.index(value)
        except ValueError:
            raise KeyError("Value \"%s\" does not exist" % value)
        return vars(self).keys()[index]

    def val(self, key):
        """
        This method returns the value for a given key.

        @param key: The key to value search
        @type key: C{string}
        
        
        @return: The value associated with the given key
        @rtype: C{int}
        """
        return vars(self)[key]

    def _parse(self, names):
        """
        This private method checks an incoming object and retrieves the names
        contained within the object.

        @param names: The object containing key names
        @type names: 
        

        @return: The given name(s)
        @rtype: C{string} or C{list} of C{string}s
        """
        ### If names is a string, parse it as a list of names.
        if type(names) == type(""):
            return names.split()
        else:
            return names
