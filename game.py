from constants import *
from paddle import Paddle
from ball import Ball
from perlin_variate import PerlinVariate
from perlin_line import PerlinLine

class Game(object):
    __slots__ = "ball paddles bg_perl perl_line excitement gameover score".split()
    
    def __init__(self):
        self.ball = Ball(width * 0.5, 100, 255, 0, 255)
        self.paddles = [Paddle(width * 0.5, PADDLE_DEFAULT_OFFSET, 0, 255, 0, 0, LEFT, RIGHT),
                        Paddle(width * 0.5, height - PADDLE_DEFAULT_OFFSET, PI, 0, 0, 255, LEFT, RIGHT),

                        # the walls
                        Paddle(-5, height * 0.5, HALF_PI + PI, 0, 255, 0, None, None, w=height * 1.2, h=20, is_round=False),
                        Paddle(width + 5, height * 0.5, HALF_PI, 255, 255, 0, None, None, w=height * 1.2, h=20, is_round=False)]
        self.bg_perl = PerlinVariate(BACKGROUND_PERLIN_SPEED)
        self.perl_line = PerlinLine(width * 0.5)
        self.excitement = 0
        self.gameover = False
        self.score = 0

    def update(self, pressed_keys):
        self.bg_perl.update()
        self.perl_line.update(self.excitement)
        for paddle in self.paddles:
            paddle.update(pressed_keys)
        if not self.gameover:
            self.excitement *= EXCITEMENT_DECAY
            self.score += 1
            try:
                self.ball.update(self.paddles)
            except Collision:
                self.excitement = 1
            except GameOver:
                self.gameover = True
                self.excitement = 3
    
    def draw(self):
        background(self.bg_perl.query(*BACKGROUND_PERLIN_RANGE))
        fill(255)
        stroke(255)
        text(self.score, 30, 30)
        translate(0, height)
        scale(1, -1)
        self.perl_line.draw(self.excitement)
        for paddle in self.paddles:
            paddle.draw()
        self.ball.draw()
    
    