from pico2d import *
from header import *


pico2d.open_canvas(WIDTH, HEIGHT)
collections.initialize()


running = True

def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            if event.type in (SDL_KEYDOWN,SDL_KEYUP):
                player.handle_event(event) # input event

# game loop
while running:
    pico2d.clear_canvas()
    player.update_time(0.01)
    player.update()
    player.draw_animation(collections)

    pico2d.update_canvas()

    handle_events()



pico2d.close_canvas()
