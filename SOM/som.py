import nessi_vector

class SOM:

    def __init__(self,length=0,):
        x_length=length
        if(x_length>0):
            x_length+=1

        self.x  = nessi_vector.NessiVector(x_length)
        self.y  = nessi_vector.NessiVector(length)
        self.dy = nessi_vector.NessiVector(length)
        self.x_units
        self.y_units

    def __len__(self):
        return len(self.y)
