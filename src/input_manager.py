from pico2d import *


class InputManager:

    def __init__(self):
        self.right = False
        self.left = False
        self.jump = False
        self.slash = False

    def on_keyboard_event(self,e:Event):
        if e.type == SDL_KEYDOWN:
            if e.key == SDLK_SPACE:
                self.jump = True
            elif e.key == SDLK_RIGHT:
                self.right = True
            elif e.key == SDLK_LEFT:
                self.left = True
            elif e.key == SDLK_a:
                self.slash = True

        elif e.type ==SDL_KEYUP:
            if e.key == SDLK_SPACE:
                self.jump = False
            elif e.key == SDLK_RIGHT:
                self.right = False
            elif e.key == SDLK_LEFT:
                self.left = False
            elif e.key == SDLK_a:
                self.slash = False
