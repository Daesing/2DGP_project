from pico2d import *
import game_framework
import logo_mode
from game_world import collections
WIDTH = 1280
HEIGHT = 720

pico2d.open_canvas(WIDTH, HEIGHT)
collections.initialize()
# game loop
game_framework.run(logo_mode)

pico2d.close_canvas()
