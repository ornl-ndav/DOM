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

class Information(object):
    """
    This is a collector class used for storing information that is not pure
    instrument geometry information. The class contains members for a list
    of values, a list of errors and an index selector object. This object
    will be used for things like detector efficiencies, energy offset
    corrections (BSS), final wavelengths (BSS) and other pieces of information
    of this sort.

    @ivar __value__: The values associated with the information to be stored
    @type __value__: C{list} of C{tuple}s or C{tuple}

    @ivar __err2__: The square uncertainties associated with the values 
    @type __err2__: C{list} of C{tuple}s or C{tuple}

    @ivar __units__: The units associated with the information
    @type __units__: C{string}

    @ivar __selector__: The index selector that is appropriate for retrieving
                        the stored information.
    @type __selector__: L{IndexSelectorBase}
    """
    
    def __init__(self, value, err2, units, selector, **kwargs):
        """
        Class constructor
        
        @param value: The values associated with the information
        @type value: C{list} of C{tuple}s or C{tuple}
        
        @param err2: The uncertainties squared associated with the values
        @type err2: C{list} of C{tuple}s or C{tuple}
        
        @param selector: The name of an index selector
        @type selector: C{string}
        
        @param kwargs: A list of key word arguments. This list is reserved for
        the use of passing key words arguments to the index selector.
        """
        import indexselector 
        
        self.__value__ = value
        self.__err2__ = err2
        self.__units__ = units
        self.__selector__ = indexselector.getIndexSelector(selector, **kwargs)

    def get_value(self, id, **kwargs):
        """
        This function returns a tuple containing the value and error2
        processed from the selector via the given id. If no error2 list is
        present, the error2 given in the returned tuple is 0.

        @param id: An object containing the pixel ID to be checked by the index
                   selector
        @type id: L{SOM.SO}
        

        @returns: The value and error2 associated with the given id
        @rtype: C{tuple}
        

        @exception RuntimeError: No index selector was provided to the object
        @exception RuntimeError: No value list was provided to the object
        """
        try:
            offset = self.__selector__.getIndex(id)
        except AttributeError:
            raise RuntimeError("Do not have information for selecting value")

        try:
            val = self.__value__[offset]
        except TypeError, e:
            if "unscriptable" in str(e) or "unsubscriptable" in str(e):
                val = self.__value__
            else:
                raise RuntimeError("Do not have information for value")

        try:
            err2 = self.__err2__[offset]
        except TypeError, e:
            if "unscriptable" in str(e) or "unsubscriptable" in str(e):
                if self.__err2__ is not None:
                    err2 = self.__err2__
                else:
                    err2 = 0.0
            else:
                err2 = 0.0

        return (val, err2, self.__units__)

    def __str__(self):
        import os

        result = []
        
        result.append("Units: %s\tSelector: %s" % (self.__units__,
                                                   self.__selector__))

        try:
            length = len(self.__value__)
            result.append("Value: %s" % self.__value__.__str__(length))
            result.append("Error^2: %s" % self.__err2__.__str__(length))
        except TypeError:
            result.append("Value: %s" % str(self.__value__))
            result.append("Error^2: %s" % str(self.__err2__))            
        
        return os.linesep.join(result)
    
        
class CompositeInformation(Information):
    """
    This class creates a collection of information objects. The individual
    information objects are accessed via an internal hash according to a given
    information key. The member function call is then passed onto the
    appropriate information object.

    @ivar __inst_hash: Hash table for L{Information} objects for different
                       banks of a full instrument.
    @type __inst_hash: C{dict}    
    """
    
    def __init__(self, *args, **kwargs):
        """
        Constructor for class. 

        @param args: Listing of key, information pairs
        @type args: C{string}, L{Information}, etc.
        
        @param kwargs: A list of key word arguments that the constructor
                       accepts
        
        @keyword pairs: Listing of key, information pairs
        @type pairs: C{list} of C{string}, L{Information} pairs
        """
        self.__info_hash = {}

        pairlist = []
        if args:
            if len(args) % 2 != 0:
                raise RuntimeError("The list of arguments must be pairwise "\
                                   +"and proceed as: key1, info1, "\
                                   +"key2, info2 ...")
            # Everything is OK, go on
            else:
                pass

            pairlist.extend(args)

        else:
            try:
                pairlist = kwargs["pairs"]
            # If key is not present, don't do anything
            except KeyError:
                pass

        if pairlist:
            for i in range(0,len(pairlist),2):
                self.__info_hash[pairlist[i]] = pairlist[i+1]
        # No arguments or keywords given, do nothing
        else:
            pass
        
    def set_information(self, key, obj):
        """
        This method sets the information object to the given key name in the
        internal hash.

        @param key: The given key name for the information
        @type key: C{string}
        
        @param obj: The given information object
        @type obj: L{Information}
        """
        self.__info_hash[key] = obj

    def get_information(self, key, **kwargs):
        """
        This method returns the information assigned to the given key in the
        internal hash.

        @param key: The given key name for the information
        @type key: C{string}
        
        @param kwargs: A list of key word arguments that the method accepts


        @returns: The information object associated with the given key
        @rtype: L{Information}
        """
        return self.__info_hash[key]

    def get_value(self, id, **kwargs):
        """
        This method obtains the value, error2 tuple from the information
        object.

        @param id: The object containing the pixel ID
        @type id: L{SOM.SO}
        
        @param kwargs: A list of key word arguments that the method accepts


        @returns: The value and its associated error^2 for the requested
                  information object
        @rtype: C{tuple}
        """
        return self.__info_hash[id[0]].get_value(id, **kwargs)

    def __str__(self):
        """
        This method returns the string representation of the
        C{CompositeInformation} object.

        @returns: The string representation of the object
        @rtype: C{string}
        """
        import os

        result = []

        for key in self.__info_hash.keys():
            result.append("%s: %s" % (key, str(self.__info_hash[key])))

        return os.linesep.join(result)

if __name__ == "__main__":
    import nessi_list

    val = nessi_list.NessiList()
    err2 = nessi_list.NessiList()

    val.extend(1.0,2.0)
    err2.extend(0.5,0.4)

    info1 = Information(val, None, "meter", "ZSelector")

    print "Info:",info1

    info2 = Information(val, err2, "meter", "ZSelector")

    comp = CompositeInformation("bank1", info1, "bank2", info2)

    print "CompInfo:",comp
