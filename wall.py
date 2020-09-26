import pygame
from hitbox import Hitbox
from utils import tuple_sum
from Vector import Vec

class Wall(Hitbox):

    def __init__(self, screen, position, width, height, color, ident=None):
        self.position = position
        if width < 0:
            self.position = self.position + Vec(width,0)
            width *= -1
        if height < 0:
            self.position = self.position + Vec(0, height)
            height *= -1
        self.width = width
        self.height = height
        self.screen = screen
        self.color = color
        pygame.draw.rect(self.screen, self.color, pygame.Rect(tuple(self.position), (self.width, self.height)))
        super().__init__(self.position, self.position+Vec(width,height),ident)
    
    def blank(self):
        pass
    
    def update(self, hitboxes):
        # pygame.draw.rect(self.screen, self.color, pygame.Rect(tuple(self.position), (self.width, self.height)))
        pass

    def get_hitbox(self):
        return Hitbox((self.position[0], self.position[1]), (self.position[0]+self.width, self.position[1]+self.height), self.ident)

    def __repr__(self):
        return self.ident

    def __hash__(self):
        return hash(self.ident)

    def __eq__(self, other):
        return self.ident == other.ident