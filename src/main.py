from entity import *
from pico2d import *

collections = SpriteCollection()

def main():
    pico2d.open_canvas(1280, 720)

    collections.initialize()

    running = True
    player = Knight(400, 200)


    while running:
        pico2d.clear_canvas()

        player.update(0.01)
        player.draw_animation(collections)

        pico2d.update_canvas()

        for event in pico2d.get_events():
            if event.type == pico2d.SDL_QUIT:
                running = False


    pico2d.close_canvas()


if __name__ == "__main__":
    main()
