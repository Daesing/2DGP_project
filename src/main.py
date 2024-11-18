from pico2d import *
from game_world import collections
import logo_mode, game_framework
import logo_mode as start_mode
from header import WIDTH, HEIGHT


pico2d.open_canvas(WIDTH, HEIGHT)
collections.initialize()
# game loop
game_framework.run(start_mode)

pico2d.close_canvas()
