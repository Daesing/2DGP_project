from pico2d import *

import game_framework
import game_world
import title_mode
from knight import Knight


def init():
    global knight
    knight = Knight(300,200)

    game_world.add_object(knight,1)

def handle_events():

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        else:
            knight.handle_event(event)

def update():
    game_world.update()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def finish():
    game_world.clear()
    pass
def pause(): pass
def resume(): pass

