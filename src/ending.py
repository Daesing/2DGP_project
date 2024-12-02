from pico2d import load_image, get_events, clear_canvas, update_canvas, load_music
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE, SDLK_RETURN

import game_framework
from header import WIDTH,HEIGHT
import title_mode


def init():
    global image,bgm
    image = load_image('../resource/background/ending_scene.png')
    bgm = load_music('../resource/audio/bgm/Ending.wav')
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
        elif (event.type,event.key) == (SDL_KEYDOWN,SDLK_RETURN):
            bgm.stop()
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