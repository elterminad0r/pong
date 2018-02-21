from constants import *
from perlin_variate import PerlinVariate

def in_bounds(vec):
    return 0 <= vec.x <= width and 0 <= vec.y <= height

class Paddle(object):
    __slots__ = """pos mov_vector normal_vector l_mov r_mov angle colour colour_perl_var
                   left_key right_key w h h_w h_h l_corner r_corner is_round excitement""".split()

    def __init__(self, x, y, angle, r, g, b, left_key, right_key, w=PADDLE_DEFAULT_WIDTH, h=PADDLE_DEFAULT_HEIGHT, is_round=True):
        self.pos = PVector(x, y)
        self.mov_vector = PVector.fromAngle(angle)
        self.normal_vector = PVector.fromAngle(angle + HALF_PI)
        self.l_mov = PVector.mult(self.mov_vector, -PADDLE_MOVEMENT_STEP)
        self.r_mov = PVector.mult(self.mov_vector, PADDLE_MOVEMENT_STEP)
        self.angle = angle
        self.colour = color(r, g, b)
        self.colour_perl_var = PerlinVariate(NEON_COLOUR_PERLIN_SPEED)
        self.left_key = left_key
        self.right_key = right_key
        self.w = w
        self.h = h
        self.is_round = is_round
        self.h_w = w * 0.5
        self.h_h = h * 0.5
        self.l_corner = self.pos + PVector.mult(self.mov_vector, -self.h_w)
        self.r_corner = self.pos + PVector.mult(self.mov_vector, self.h_w)
        self.excitement = 0

    def update(self, pressed_keys):
        self.excitement *= EXCITEMENT_DECAY
        self.colour_perl_var.update()
        op = False
        if pressed_keys[self.left_key] and in_bounds(self.l_corner):
            op = self.l_mov
        elif pressed_keys[self.right_key] and in_bounds(self.r_corner):
            op = self.r_mov
        if op:
            for vec in self.pos, self.l_corner, self.r_corner:
                vec += op

    def ball_collides(self, ball):
        return (abs((ball.pos - self.pos).dot(self.mov_vector)) < self.h_w and
                -2 * ball.r < ((ball.pos - self.pos).dot(self.normal_vector)) < ball.r + self.h_h + COLLISION_FUZZ and
                ball.vel.dot(self.normal_vector) < 0)

    def draw(self):
        pushMatrix()
        translate(self.pos.x, self.pos.y)
        rotate(self.angle)
        noStroke()
        fill(lerpColor(self.colour, WHITE, self.colour_perl_var.query(*(ratio + self.excitement for ratio in NEON_FILL_LERP_RATIO_RANGE))))
        rect(0, 0, self.w, self.h)
        stroke(self.colour)
        strokeWeight(PADDLE_DEFAULT_STROKE)
        line(-self.h_w, self.h_h, self.h_w, self.h_h)
        line(-self.h_w, -self.h_h, self.h_w, -self.h_h)
        arc(-self.h_w, 0, self.h_h, self.h_h, HALF_PI, PI + HALF_PI, OPEN)
        rotate(PI)
        arc(-self.h_w, 0, self.h_h, self.h_h, HALF_PI, PI + HALF_PI, OPEN)
        popMatrix()