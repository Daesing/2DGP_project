from pico2d import load_image, get_events, clear_canvas, update_canvas
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE, SDLK_RETURN, SDLK_1, SDLK_2

import game_framework
import lobby
from header import WIDTH,HEIGHT
import title_mode
import stage1, stage2


def init():
    global image
    image = load_image('resource/background/game_over.png')


def finish():
    global image
    del image


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_1:
            game_framework.change_mode(stage1)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_2:
            game_framework.change_mode(stage2)
        elif (event.type,event.key) == (SDL_KEYDOWN,SDLK_RETURN):
            game_framework.change_mode(title_mode)

    pass


def update():
    pass

def draw():
    clear_canvas()
    image.draw(WIDTH//2, HEIGHT//2)
    update_canvas()
    pass

def pause(): pass
def resume(): pass