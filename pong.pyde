from collections import defaultdict

from game import Game

pressed_keys = defaultdict(bool)

def setup():
    global game, f
    size(800, 800)
    rectMode(CENTER)
    ellipseMode(RADIUS)
    game = Game()
    f = createFont("courier", 20)

def draw():
    textFont(f, 20)
    game.update(pressed_keys)
    game.draw()

def keyPressed():
    pressed_keys[keyCode] = True
    if keyCode == ord("R"):
        game.__init__()

def keyReleased():
    pressed_keys[keyCode] = False
