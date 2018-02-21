from constants import *
from perlin_variate import PerlinVariate

class PerlinLine(object):
    __slots__ = "mid_y line_perl".split()
    def __init__(self, mid_y):
        self.mid_y = mid_y
        self.line_perl = PerlinVariate(LINE_PERLIN_SPEED)

    def update(self, excitement):
        self.line_perl.accelerate(LINE_PERLIN_SPEED * (1 + excitement))

    def draw(self, excitement):
        noFill()
        stroke(255, LINE_ALPHA)
        strokeWeight(3)
        beginShape()
        for x in range(0, width + LINE_XSTEP, LINE_XSTEP):
            y_range = height * LINE_PERLIN_YRANGE_RATIO * (1 + excitement)
            vertex(x, self.mid_y + self.line_perl.query(-y_range, y_range, x * LINE_PERLIN_XRATIO))
        endShape()