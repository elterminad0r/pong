from constants import *

class PerlinVariate(object):
    __slots__ = "speed t ".split()

    def __init__(self, speed):
        self.speed = speed
        self.t = random(PERLIN_START_RANGE)
    
    def update(self):
        self.t += self.speed
    
    def accelerate(self, speed):
        self.t += speed
    
    def query(self, lo, hi, *coordinates):
        return map(noise(self.t, *coordinates), 0, 1, lo, hi)