

class Hitbox:

    def __init__(self, point1, point2, ident=None):
        self.x1 = point1[0]
        self.y1 = point1[1]
        self.x2 = point2[0]
        self.y2 = point2[1]
        self.ident=ident

    def contains(self, other): # Base case for rectangular hitboxes
        if self.y1 >= other.y2 or self.y2 <= other.y1: # One rectangle is completly above the other
            return False
        elif self.x1 >= other.x2 or self.x2 <= other.x1: # One rectangle completly to the left of the other 
            return False
        else:
            return True

    def __eq__(self, other):
        return self.ident == other.ident
        # return (self.x1 == other.x1 and self.x2 == other.x2 and self.y1 == other.y1 and self.y2 == other.y2)
    
    def __hash__(self):
        return hash(self.ident)

    def __repr__(self):
        return self.ident
    