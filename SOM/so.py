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
    """
    
    def __init__(self,dim=1,id=None,**kwargs):

        if kwargs.has_key("construct"):
            self.y     = nessi_list.NessiList()
            self.var_y = nessi_list.NessiList()
        else:
            self.y     = None
            self.var_y = None
        self.id    = id
        self.axis = []
        for i in range(dim):
            self.axis.append(PrimaryAxis(i+1,**kwargs))
        self.__dim = dim

    def dim(self):
        return self.__dim

    def __len__(self):
        return len(self.y)

    def __str__(self):
        if self.id == None:
            return "(None, "+str(self.axis)+", "+str(self.y)+\
                   ", "+str(self.var_y)+")"
        else:
            return "("+str(self.id)+", "+str(self.axis)+", "+str(self.y)+\
                   ", "+str(self.var_y)+")"

    def __repr__(self):
        return self.__str__()

    def __eq__(self,other):
        try:
            if self.y != other.y:
                return False

            if self.var_y != other.var_y:
                return False
            
            if len(self.axis) != len(other.axis):
                return False

            for axis_self,axis_other in map(None,self.axis,other.axis):
                if axis_self != axis_other:
                    return False

        except:
            return False

        return True

    def __ne__(self,other):
        return not self.__eq__(other)


class PrimaryAxis:
    
    def __init__(self,id=1,**kwargs):

        if kwargs.has_key("construct"):
            self.val = nessi_list.NessiList()
        else:
            self.val = None
        if kwargs.has_key("withVar"):
            if kwargs.has_key("construct"):
                self.var = nessi_list.NessiList()
            else:
                self.var = None
        else:
            self.var = None
        self.pid = id

    def __len__(self):
        return len(self.val)

    def __str__(self):
        if self.var==None:
            return "("+str(self.pid)+", "+str(self.val)+")"
        else:
            return "("+str(self.pid)+", "+str(self.val)+", "\
                   +str(self.var)+")"

    def __repr__(self):
        return self.__str__()

    def __eq__(self,other):
        try:
            if self.val != other.val:
                return False

            if(self.var != None and other.var != None):
                if self.var != other.var:
                   return False
               
        except:
            return False

        return True

    def __ne__(self,other):
        return not self.__eq__(other)
    
        
if __name__ == "__main__":
    so1 = SO(construct=True, withVar=True)
    so1.axis[0].val.extend([1.0,2.0,3.0])
    so1.axis[0].var.extend([1.0,2.0,3.0])
    so1.y.extend([40.0,55.0])
    so1.var_y.extend([40.0,55.0])
    so1.id="Pixel 1"
    print "1D SO:", so1

    so2 = SO(construct=True, withVar=True)
    so2.axis[0].val.extend([1.0,2.0,3.0])
    so2.axis[0].var.extend([1.0,2.0,3.0])
    so2.y.extend([60.0,65.0])
    so2.var_y.extend([60.0,65.0])
    so2.id="Pixel 2"
    print "1D SO:", so2

    if so1 == so2:
        print "Is equals"
    else:
        print "Not equal"
