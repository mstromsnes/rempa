import pygame
from ball import Ball
from paddle import Paddle
from wall import Wall
from time import sleep
from math import sqrt, tau, sin, cos
from random import random, randint
from Vector import Vec
SCALE_FACTOR = 4

class Pong:

    BG_COLOR = pygame.Color('black')
    WIDTH = 400*SCALE_FACTOR
    HEIGHT = 201*SCALE_FACTOR
    BORDER = 20
    VELOCITY = 2
    RADIUS = 8*SCALE_FACTOR
    BALLCOUNT = 10*SCALE_FACTOR
    SUPER_SAMPLING = 4

    def __init__(self, fg_color):
        self.screen = pygame.display.set_mode((self.WIDTH,self.HEIGHT))
        Wall(self.screen, Vec(0,0), self.WIDTH, self.HEIGHT, pygame.Color('Blue'))
        self.fg_color = fg_color
        left_wall = Wall(self.screen, Vec(0,0), self.BORDER, self.HEIGHT, fg_color, ident='left_wall')
        top_wall = Wall(self.screen, Vec(0,0), self.WIDTH, self.BORDER, fg_color, ident='top_wall')
        right_wall = Wall(self.screen, Vec(self.WIDTH, 0), -self.BORDER, self.HEIGHT, fg_color, ident='right_wall')
        bottom_wall = Wall(self.screen, Vec(0, self.HEIGHT), self.WIDTH, -self.BORDER, fg_color, ident='bottom_wall')
        # self.objects = [left_border, top_border, right_border, bottom_border]
        self.objects = {
            left_wall: left_wall,
            top_wall: top_wall,
            right_wall: right_wall,
            bottom_wall: bottom_wall
            }
        for i in range(0,self.BALLCOUNT):
            self.spawn_ball(i)

    def spawn_ball(self, i):
        angle = random()*tau
        radius = int(self.RADIUS*(2*random()+0.2))
        speed = Vec(self.VELOCITY*cos(angle)/self.SUPER_SAMPLING,
                    self.VELOCITY*sin(angle)/self.SUPER_SAMPLING)
        position = Vec(randint(self.BORDER+radius, self.WIDTH-self.BORDER-radius),
                        randint(self.BORDER+radius, self.HEIGHT-self.BORDER-radius))
        ident = f"ball{i}"
        for obj in self.objects:
            if obj.get_hitbox().contains(Ball.ball_hitbox(position, radius)):
                self.spawn_ball(i)
                return
        ball = Ball(self.screen, position, speed, radius, self.fg_color, self.BG_COLOR, ident)
        self.objects.update({ball: ball})


    def update(self):
        self.blank()
        for obj in self.objects:
            if isinstance(obj, Wall):
                continue
            obj.update(self.objects)

    def blank(self):
        for obj in self.objects:
            obj.blank()



if __name__ == "__main__":
    pygame.init()

    fg_color = pygame.Color('white')
    pong = Pong(fg_color)
    while True:
        e = pygame.event.poll()
        if e.type == pygame.QUIT:
            break
        for _ in range(0,pong.SUPER_SAMPLING):
            pong.update()
        pygame.display.flip()
        # sleep(0.005)

