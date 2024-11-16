from pico2d import *


class InputManager:

    def __init__(self):
        self.right = False
        self.left = False
        self.jump = False
        self.up = False
        self.slash = False
        self.dash = False

    def on_keyboard_event(self,e:Event):
        if e.type == SDL_KEYDOWN:
            if e.key == SDLK_SPACE:
                self.jump = True
            elif e.key == SDLK_RIGHT:
                self.right = True
            elif e.key == SDLK_LEFT:
                self.left = True
            elif e.key == SDLK_UP:
                self.up = True
            elif e.key == SDLK_a:
                self.slash = True
            elif e.key == SDLK_d:
                self.dash = True

        elif e.type ==SDL_KEYUP:
            if e.key == SDLK_SPACE:
                self.jump = False
            elif e.key == SDLK_RIGHT:
                self.right = False
            elif e.key == SDLK_LEFT:
                self.left = False
            elif e.key == SDLK_UP:
                self.up = False
            elif e.key == SDLK_a:
                self.slash = False
            elif e.key == SDLK_d:
                self.dash = False
