from pico2d import *
from header import *

pico2d.open_canvas(WIDTH, HEIGHT)
collections.initialize()

# game loop
while world.is_running():
    world.update(0.01)
    world.render_entity()

pico2d.close_canvas()
