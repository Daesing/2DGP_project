from pico2d import load_image, get_events, clear_canvas, update_canvas, load_music
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE

import game_framework
import lobby


def init():
    global image,bgm
    image = load_image('../resource/background/game_title.png')
    bgm = load_music('../resource/audio/bgm/Title.wav')
    bgm.set_volume(30)
    bgm.repeat_play()


def finish():
    global image,bgm
    del image,bgm


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type,event.key) == (SDL_KEYDOWN,SDLK_SPACE):
            bgm.stop()
            game_framework.change_mode(lobby)


    pass


def update():
    pass


def draw():
    clear_canvas()
    image.draw(1280//2, 720//2)
    update_canvas()
    pass

def pause(): pass
def resume(): pass