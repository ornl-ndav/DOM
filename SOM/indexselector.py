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

class IndexSelectorBase:
    """
    This is the C{IndexSelectorBase} abstract base class. It serves as the
    foundation for an index selector concrete class. All concrete classes must
    override both the constructor and the getIndex member function. The id
    passed to the getIndex function is interpreted based on the implementation
    provided by the concrete class. The format of the id object that the
    concrete classes should expect to work on are of the form:
    (\"bankN\", (i, j)) which is a tuple containing a string and a tuple of
    two numbers and where N, i and j are numbers particular to the data
    set read from a NeXus file.
    """
    
    def __init__(self, **kwargs):
        """
        Object constructor. ALL INHERITED OBJECT MUST OVERRIDE.
        """
        raise NotImplementedError("Cannot create IndexSelectorBase objects")

    def getIndex(self, id):
        """
        Method to return a given index. ALL INHERITED OBJECTS MUST OVERRIDE.
        """
        raise NotImplementedError("IndexSelectorBase objects have no " \
                                  +"selector logic")

def getIndexSelector(selector_name, **kwargs):
    """
    This is the factory function for obtaining concrete index selector objects.

    @param selector_name: The class name of the concrete index selector
    @type selector_name: C{string}
    
    @param kwargs: A list of key word arguments that the requested index
    selector will accept


    @return: The requested index selector object
    @rtype: Concrete C{IndexSelector}


    @raise Exception: If the requested index selector name is not present in
                      the factory list.
    """
    import simpleselector

    if selector_name == "ISelector":
        return simpleselector.ISelector()
    elif selector_name == "JSelector":
        return simpleselector.JSelector()
    elif selector_name == "ZSelector":
        return simpleselector.ZSelector()
    elif selector_name == "IJSelector":
        try:
            Nj_in = kwargs["Nj"]
        except KeyError:
            Nj_in = None
        return simpleselector.IJSelector(Nj=Nj_in)
    else:
        raise Exception("Do not understand selector %s" % selector_name)


