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

import nessi_list

class SO:
    """
    This class is an internal structure object responsible for keep spectral
    data together on a per pixel basis (it may be a merged set of pixels).

    @ivar id: The pixel ID for the spectral data. See L{IndexSelectorBase} for
    the standard format of the pixel ID.
    @type id: various

    @ivar y: The dependent axis of the spectral data
    @type y: C{nessi_list.NessiList}

    @ivar var_y: The square uncertainties for the dependent axis of the
                 spectral data
    @type var_y: C{nessi_list.NessiList}

    @ivar axis: The independent axes for the spectral data
    @type axis: C{list} of C{PrimaryAxis} objects

    @ivar __dim: The dimension of the spectral data
    @type __dim: C{int}
    """
    
    def __init__(self, dim=1, id=None, **kwargs):
        """
        Object constructor.

        @param dim: The desired dimension for the spectral data
        @type dim: C{int}

        @param id: The pixel ID of the spectral data
        @type id: various

        @param kwargs: A list of keyword arguments that the class accepts:

        @keyword construct: Flag to switch on the creation of the C{NessiList}s
                            for the independent and dependent axes.
        @type construct: C{boolean} 
        """
        try:
            construct = kwargs["construct"]
        except KeyError:
            construct = False

        if construct:
            self.y     = nessi_list.NessiList()
            self.var_y = nessi_list.NessiList()
        else:
            self.y     = None
            self.var_y = None
        self.id    = id
        self.axis = []
        for i in range(dim):
            self.axis.append(PrimaryAxis(i+1, **kwargs))
        self.__dim = dim

    def dim(self):
        """
        This method returns the dimension of the C{SO}.

        @return: The C{SO}s dimension
        @rtype: C{int}
        """
        return self.__dim

    def __len__(self):
        """
        This method returns the length of the C{SO}. The length is derived
        from the dependent axis.

        @return: The length of the C{SO}
        @rtype: C{int}
        """        
        return len(self.y)

    def __str__(self):
        """
        This method returns a string representation of the C{SO} object

        @return: The representation of the C{SO} object
        @rtype: C{string}
        """                
        if self.id is None:
            return "(None, "+str(self.axis)+", "+str(self.y)+\
                   ", "+str(self.var_y)+")"
        else:
            return "("+str(self.id)+", "+str(self.axis)+", "+str(self.y)+\
                   ", "+str(self.var_y)+")"

    def __repr__(self):
        """
        This method returns an instance representation of the C{SO} object

        @return: The representation of the C{SO} object
        @rtype: C{string}
        """                
        return self.__str__()

    def __eq__(self, other):
        """
        This method checks to see if the incoming C{SO} object and the
        current one are equal.

        @param other: Object to check for equality
        @type other: C{SO}


        @return: I{True} if the C{SO} objects are equal, I{False} if they
                 are not
        @rtype: C{boolean}
        """        
        try:
            if self.y != other.y:
                return False

            if self.var_y != other.var_y:
                return False
            
            if len(self.axis) != len(other.axis):
                return False

            for axis_self,axis_other in map(None, self.axis, other.axis):
                if axis_self != axis_other:
                    return False

        except:
            return False

        return True

    def __ne__(self, other):
        """
        This method checks to see if the incoming C{SO} object and the current
        one are not equal.

        @param other: Object to check for equality
        @type other: C{SO}


        @return: I{True} if the C{SO} objects are not equal, I{False} if they
                 are
        @rtype: C{boolean}
        """                
        return not self.__eq__(other)

class PrimaryAxis:
    """
    This class handles the values and error^2 arrays for an independent axis.
    The array holders (C{nessi_list.NessiList}s) are not created by default.
    The error^2 array is also not created by default.

    @ivar val: The values associated with a given independent axis
    @type val: C{nessi_list.NessiList}

    @ivar var: The squared uncertainties associated with a given independent
               axis
    @type var: C{nessi_list.NessiList}

    @ivar pid: The index ID of the primary axis. This supports N independent
               axes.
    @type pid: C{int}
    """
    
    def __init__(self, id=1, **kwargs):
        """
        Object constructor. 

        @param id: The index ID of the independent axis
        @type id: C{int}

        @param kwargs: A list of keyword arguments that the class accepts:

        @keyword construct: Flag to switch on the creation of the C{NessiList}s
        @type construct: C{boolean}

        @keyword withVar: Flag to turn on use of square uncertainties. Should
        be used in conjunction with I{construct}.
        @type withVar: C{boolean}
        """
        try:
            construct = kwargs["construct"]
        except KeyError:
            construct = False

        try:
            withVar = kwargs["withVar"]
        except KeyError:
            withVar = False

        if construct:
            self.val = nessi_list.NessiList()
        else:
            self.val = None
        if withVar:
            if construct:
                self.var = nessi_list.NessiList()
            else:
                self.var = None
        else:
            self.var = None
        self.pid = id

    def __len__(self):
        """
        This method returns the length of the C{PrimaryAxis}. The length is
        derived from the value array.

        @return: The length of the C{PrimaryAxis}
        @rtype: C{int}
        """
        return len(self.val)

    def __str__(self):
        """
        This method returns a string representation of the C{PrimaryAxis}
        object.

        @return: The representation of the C{PrimaryAxis} object
        @rtype: C{string}
        """        
        if self.var is None:
            return "("+str(self.pid)+", "+str(self.val)+")"
        else:
            return "("+str(self.pid)+", "+str(self.val)+", "\
                   +str(self.var)+")"

    def __repr__(self):
        """
        This method returns an instance representation of the C{PrimaryAxis}
        object.

        @return: The representation of the C{PrimaryAxis} object
        @rtype: C{string}
        """        
        return self.__str__()

    def __eq__(self, other):
        """
        This method checks to see if the incoming C{PrimaryAxis} object and the
        current one are equal.

        @param other: Object to check for equality
        @type other: C{PrimaryAxis}


        @return: I{True} if the C{PrimaryAxis} objects are equal, I{False} if
                 they are not
        @rtype: C{boolean}
        """
        try:
            if self.val != other.val:
                return False

            if(self.var is not None and other.var is not None):
                if self.var != other.var:
                    return False
               
        except:
            return False

        return True

    def __ne__(self, other):
        """
        This method checks to see if the incoming C{PrimaryAxis} object and the
        current one are not equal.

        @param other: Object to check for equality
        @type other: C{PrimaryAxis}


        @return: I{True} if the C{PrimaryAxis} objects are not equal, I{False}
                 if they are
        @rtype: C{boolean}
        """        
        return not self.__eq__(other)
        
if __name__ == "__main__":
    so1 = SO(construct=True, withVar=True)
    so1.axis[0].val.extend([1.0,2.0,3.0])
    so1.axis[0].var.extend([1.0,2.0,3.0])
    so1.y.extend([40.0,55.0])
    so1.var_y.extend([40.0,55.0])
    so1.id = "Pixel 1"
    print "1D SO:", so1

    so2 = SO(construct=True, withVar=True)
    so2.axis[0].val.extend([1.0,2.0,3.0])
    so2.axis[0].var.extend([1.0,2.0,3.0])
    so2.y.extend([60.0, 65.0])
    so2.var_y.extend([60.0, 65.0])
    so2.id = "Pixel 2"
    print "1D SO:", so2

    if so1 == so2:
        print "Is equals"
    else:
        print "Not equal"
