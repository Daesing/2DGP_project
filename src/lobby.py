from pico2d import *

import game_framework
import game_world
import title_mode
import stage1
from knight import Knight
from header import WIDTH,HEIGHT


def init():
    global knight
    global image,text,bgm
    image = load_image('resource/background/Dirtmouth.png')
    text = load_image('resource/ui/lobby_text.png')
    bgm = load_music('resource/audio/bgm/Lobby.wav')
    bgm.set_volume(30)
    bgm.repeat_play()
    knight = Knight(WIDTH // 2,100)
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
    if knight.x > WIDTH:
        bgm.stop()
        game_framework.change_mode(stage1)
    knight.skill_point = 9



def draw():
    clear_canvas()
    image.draw(WIDTH // 2, HEIGHT // 2)
    text.draw(1180,650)
    game_world.render()
    update_canvas()

def finish():
    global image, bgm, text
    del image, bgm, text
    game_world.clear()

def pause(): pass

def resume(): pass

