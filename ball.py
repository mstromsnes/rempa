import pygame
from hitbox import Hitbox
from utils import dot_product, tuple_sum, norm
from Vector import Vec
from wall import Wall


from math import sqrt
class Ball(Hitbox):

    def __init__(self, screen, position, speed, radius=10, fg_color=pygame.Color('White'), bg_color=pygame.Color('Black'), ident=None):
        self.position = position
        self._last_position = Vec(int(position.x), int(position.y))
        self.speed = speed
        self.acc = Vec(0, 0) # Unused
        self.fg_color = fg_color
        self.bg_color = bg_color
        self.radius = radius
        self.screen = screen
        self.show(self.position, self.fg_color)
        # self.ident = ident
        self.inside = []
        super().__init__((position[0]-self.radius, position[1]-self.radius), (position[0]+self.radius,position[1]+self.radius), ident)

    def show(self, position, color):
        x, y = position
        pygame.draw.circle(self.screen, color, (int(x), int(y)), self.radius)
        self._last_position = Vec(int(x), int(y))

    def blank(self):
        self.show(self._last_position, self.bg_color)

    def update(self, objects):
        self.blank()
        self.position += self.speed
        if self.position.int() != self._last_position:
            self.detect_collision(objects)
        if self.inside:
            self.handle_collision(self.inside)
            for other in self.inside:
                if not self.contains(other):
                    self.inside.remove(other)
        self.show(self.position, self.fg_color)

    def detect_collision(self, objects):
        for obj in objects:
            if self == obj:
                continue
            if self.contains(obj):
                self.inside.append(obj)

    def get_hitbox(self):
        x, y = self.position
        return Hitbox((x-self.radius,y-self.radius),(x+self.radius,y+self.radius), ident=self.ident)
        # return [
        #     Hitbox((self.x-self.radius, self.y-self.radius/10), (self.x+self.radius, self.y+self.radius/10), self.ident),
        #     Hitbox((self.x-self.radius/10, self.y-self.radius), (self.x+self.radius/10, self.y+self.radius), self.ident),
        #     Hitbox((self.x-self.radius/sqrt(2), self.y-self.radius/sqrt(2)), (self.x+self.radius/sqrt(2), self.y+self.radius/sqrt(2)), self.ident),
        # ]

    def __eq__(self, other):
        return self.ident == other.ident
        # return (self.x1 == other.x1 and self.x2 == other.x2 and self.y1 == other.y1 and self.y2 == other.y2)

    def __hash__(self):
        return hash(self.ident)

    def __repr__(self):
        return self.ident

    def contains(self, other):
        if isinstance(other,Ball):
            if norm(self.position-other.position) <= self.radius+other.radius:
                return True
        def distance_to_wall(ball, wall):
            distances = [
                abs(ball.position.x-wall.position.x),
                abs(ball.position.x-(wall.position.x+wall.width)),
                abs(ball.position.y-wall.position.y),
                abs(ball.position.y-(wall.position.y+wall.height)),
            ]
            return min(distances)
        if isinstance(other, Wall):
            if distance_to_wall(self, other) <= self.radius:
                return True
        return False

    def handle_collision(self, objects):

        def ball_ball_collision(self, other):
            x1, x2 = self.position, other.position
            v1, v2 = self.speed, other.speed
            m1, m2 = self.radius**3, other.radius**3
            if norm(x2-x1) > (self.radius+other.radius) or self.inside.count(other) > 1:
                return # No collision
            self.speed = v1 - ((v1-v2)@(x1-x2)/(norm(x1-x2)**2))*(x1-x2)*(2*m2/(m1+m2))
            other.speed = v2 - ((v2-v1)@(x2-x1)/(norm(x2-x1)**2))*(x2-x1)*(2*m1/(m1+m2))
            def inside(self, other):
                x1, x2 = self.position+self.speed, other.position+other.speed
                if norm(x2-x1) > (self.radius+other.radius):
                    return False
                else:
                    return True
            if not inside(self, other):
                self.inside.remove(other)


        def ball_wall_collision(self, other):
            vx, vy = self.speed
            emit = self.radius
            if other.ident == 'bottom_wall':
                self.position = Vec(self.position[0],other.position.y-emit)
                vy = -vy
            elif other.ident == 'top_wall':
                self.position = Vec(self.position[0],other.position.y+other.height+emit)
                vy = -vy
            elif other.ident == 'left_wall':
                self.position = Vec(other.position.x+other.width+emit, self.position[1])
                vx = -vx
            else:
                self.position = Vec(other.position.x-emit, self.position[1])
                vx = -vx
            self.speed = Vec(vx, vy)
            self.inside.remove(other)

        for other in objects:
            if isinstance(other, Ball):
                ball_ball_collision(self, other)
            else:
                ball_wall_collision(self, other)

    def resolve_collision(self, other):
        x1 = self.position
        v1 = self.speed
        m1 = self.radius**3
        try:
            x2 = other.position
            v2 = other.speed
            m2 = other.radius**3
            if norm(x2-x1) > (self.radius+other.radius) or other in self.inside or self in other.inside:
                return
            if not (other in self.inside or self in other.inside):
                self.inside.append(other)
                other.inside.append(self)
            self.speed = v1 - ((v1-v2)@(x1-x2)/(norm(x1-x2)**2))*(x1-x2)*(2*m2/(m1+m2))
            other.speed = v2 - ((v2-v1)@(x2-x1)/(norm(x2-x1)**2))*(x2-x1)*(2*m1/(m1+m2))
        except (TypeError, AttributeError):
            # s_hitbox = self.get_hitbox()
            s_vx, s_vy = self.speed
            # if s_hitbox.x1 > o_hitbox.x1 and s_hitbox.x2 < o_hitbox.x2: # Hitting a horizontal edge
            #     s_vy = -s_vy
            # if s_hitbox.y1 > o_hitbox.y1 and s_hitbox.y2 < o_hitbox.y2: # Hitting a vertical edge
            #     s_vx = -s_vx
            emit = self.radius
            if other.ident == 'bottom_wall':
                self.position = Vec(self.position[0],other.position.y-emit)
                s_vy = -s_vy
            elif other.ident == 'top_wall':
                self.position = Vec(self.position[0],other.position.y+emit)
                s_vy = -s_vy
            elif other.ident == 'left_wall':
                self.position = Vec(other.position.x+emit, self.position[1])
                s_vx = -s_vx
            else:
                self.position = Vec(other.position.x-emit, self.position[1])
                s_vx = -s_vx

            self.speed = Vec(s_vx, s_vy)

    @classmethod
    def ball_hitbox(cls, position, radius):
        return Hitbox((position.x-radius, position.y-radius),(position.x+radius,position.y+radius))


            # if self.vx > 0:
            #     if not (hitbox.x1 > other.x1 and hitbox.x2 < other.x2):
            #         if hitbox.x2 > other.x1:
            #             self.vx *= -1
            # else hitbox.x1 > other.x2:
            #     self.vx *= -1
            # if self.vy > 0:
            #     if hitbox.y2 > other.y1:
            #         self.vy *= -1
            # elif hitbox.y1 > other.y2:
            #     self.vy *= -1
