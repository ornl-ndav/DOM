import nessi_vector

class SO:

    def __init__(self):
        self.x     = nessi_vector.NessiVector(length)
        self.y     = nessi_vector.NessiVector(length)
        self.var_y = nessi_vector.NessiVector(length)
        self.id    = 0

    def __len__(self):
        return len(self.y)
