from random import choice

from constants import *
from perlin_variate import PerlinVariate

class Ball(object):
    __slots__ = "pos colour speed vel r rad_perl_var colour_perl_var excitement".split()

    def __init__(self, x, y, r, g, b, speed=BALL_DEFAULT_SPEED, angle=BALL_DEFAULT_ANGLE, radius=BALL_DEFAULT_RADIUS):
        self.pos = PVector(x, y)
        self.colour = color(r, g, b)
        self.speed = speed
        self.vel = PVector.mult(PVector.fromAngle(angle + random(*BALL_START_ABBERATION_RANGE) * choice([1, -1])), speed)
        self.r = radius
        self.rad_perl_var = PerlinVariate(BALL_PERLIN_SPEED)
        self.colour_perl_var = PerlinVariate(NEON_COLOUR_PERLIN_SPEED)
        self.excitement = 0

    def hit_edge(self):
        return (self.pos.x < self.r or
                self.pos.x > width - self.r or
                self.pos.y < self.r or
                self.pos.y > height - self.r)

    def update(self, paddles):
        self.excitement *= EXCITEMENT_DECAY
        self.rad_perl_var.update()
        self.colour_perl_var.update()
        self.pos += self.vel
        if self.hit_edge():
            raise GameOver
        for paddle in paddles:
            if paddle.ball_collides(self):
                paddle.excitement = 1
                if paddle.is_round:
                    offset = (self.pos - paddle.pos).dot(paddle.mov_vector)
                    self.vel = PVector.mult(PVector.fromAngle(paddle.angle + HALF_PI -
                                                              map(offset, -paddle.h_w, paddle.h_w,
                                                                        -BALL_MAX_REFLECT_MAG, BALL_MAX_REFLECT_MAG)),
                                            self.speed)
                else:
                    self.vel += PVector.mult(paddle.normal_vector, -2 * self.vel.dot(paddle.normal_vector))
                raise Collision
    
    def draw(self):
        fill(lerpColor(self.colour, WHITE, self.colour_perl_var.query(*(ratio + self.excitement for ratio in NEON_FILL_LERP_RATIO_RANGE))))
        stroke(self.colour)
        strokeWeight(BALL_DEFAULT_STROKE)
        displayed_r = self.rad_perl_var.query(*(self.r * ratio for ratio in BALL_PERLIN_RANGE))
        ellipse(self.pos.x, self.pos.y, displayed_r, displayed_r)