from pico2d import *


class StateManager:

    def __init__(self):
        self.right = False
        self.left = False
        self.jump = False
        self.slash = False
        self.time_out = False

    def on_keyboard_event(self,e):
        self.time_out = False
        if e[0] != 'INPUT':
            return
        if e[1].type == SDL_KEYDOWN:
            if e[1].key == SDLK_SPACE:
                self.jump = True
            elif e[1].key == SDLK_RIGHT:
                self.right = True
            elif e[1].key == SDLK_LEFT:
                self.left = True
            elif e[1].key == SDLK_a:
                self.slash = True

        elif e[1].type ==SDL_KEYUP:
            if e[1].key == SDLK_SPACE:
                self.jump = False
            elif e[1].key == SDLK_RIGHT:
                self.right = False
            elif e[1].key == SDLK_LEFT:
                self.left = False
            elif e[1].key == SDLK_a:
                self.slash = False
