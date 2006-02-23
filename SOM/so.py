import nessi_vector

class SO:

    def __init__(self):
        self.x     = nessi_vector.NessiVector(0)
        self.y     = nessi_vector.NessiVector(0)
        self.var_y = nessi_vector.NessiVector(0)
        self.id    = None

    def __len__(self):
        return len(self.y)
