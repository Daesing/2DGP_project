from pico2d import *

import game_framework
import game_world
import title_mode
from knight import Knight
import play_mode

# knight 객체의 생성이 스테이지마다 이루어지면 위치를 어떻게 설정하는가?
def init():
    global stage1_back
    stage1_back = load_image('../resource/Forgotten_Crossroads_False_Knight_Arena.png')
    global knight
    knight = Knight(0)
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
    stage1_back.draw(1280 // 2, 720 // 2)
    game_world.render()
    update_canvas()

def finish():
    game_world.clear()
    pass
def pause(): pass
def resume(): pass

