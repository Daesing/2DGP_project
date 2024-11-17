from pico2d import *

import game_framework
import game_world
import title_mode
import stage1
from knight import Knight
from header import WIDTH,HEIGHT


def init():
    global knight
    global image,text
    image = load_image('../resource/background/Greenpath_Hornet_Arena.png')
    text = load_image('../resource/ui/stage2_text.png')
    knight = Knight(0,140)
    game_world.add_object(knight, 1)

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
    if knight.x < 0:
        game_framework.change_mode(stage1)



def draw():
    clear_canvas()
    image.draw(WIDTH // 2, HEIGHT // 2)
    text.draw(1150,650)
    game_world.render()
    update_canvas()

def finish():
    game_world.clear()
    pass
def pause(): pass
def resume(): pass

