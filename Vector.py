from math import sqrt
from utils import norm

class Vec:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        if isinstance(other, (int, float)):
            return Vec(self.x+other, self.y+other)
        return Vec(self.x+other.x,self.y+other.y)
    
    def __sub__(self, other):
        if isinstance(other, (int, float)):
            return Vec(self.x-other, self.y-other)
        return Vec(self.x-other.x,self.y-other.y)
    
    def __mul__(self, other):
        return Vec(self.x*other, self.y*other)
    
    def __matmul__(self, other):
        if isinstance(other, (int, float)):
            return self*other
        return self.x*other.x+self.y*other.y
    
    def __rmatmul__(self, other):
        return self@other

    def __rmul__(self, other):
        return self*other

    def __neg__(self):
        return Vec(-self.x, -self.y)
    
    def int(self):
        return Vec(int(self.x), int(self.y))

    def __iter__(self):
        self.n = 0
        return self
    
    def __next__(self):
        self.n += 1
        if self.n == 1:
            return self.x
        elif self.n == 2:
            return self.y
        else:
            raise StopIteration
    
    def __getitem__(self, item):
        if item == 0:
            return self.x
        if item == 1:
            return self.y
    
    def norm(self):
        norm = 0
        for e in self:
            norm += e**2
        return sqrt(norm)
    
    def __repr__(self):
        return f"x: {self.x}, y: {self.y}"