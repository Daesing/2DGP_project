from animation import SpriteCollection
from state_machine import StateMachine, AnimationState
from typing import Self


class Entity:

    def __init__(self, x, y, state: AnimationState[Self], ratio=1.0):
        self.current_animation = None
        self.x = x
        self.y = y
        self.ratio = ratio
        self.animation_time = 0
        self.inverted = False
        self.state_machine = StateMachine(self)
        self.state_machine.start(state)

    def set_animation(self, animation: str, inverted=False):
        self.current_animation = animation
        self.inverted = inverted
        self.animation_time = 0
        print(f'{self.current_animation} inverted: {self.inverted}')

    def draw(self, collections: SpriteCollection):
        animation = collections.get(self.current_animation)
        sprite_width, sprite_height = animation.get_size()
        draw_width, draw_height = sprite_width * self.ratio, sprite_height * self.ratio
        animation.draw(self.x, self.y, self.animation_time, self.inverted, draw_width, draw_height)

    def update(self):
        self.animation_time += 0.01

    def get_size(self, collections: SpriteCollection):
        animation = collections.get(self.current_animation)
        sprite_width, sprite_height = animation.get_size()
        draw_width, draw_height = sprite_width * self.ratio, sprite_height * self.ratio
        return draw_width, draw_height

    def get_boundary(self, collections: SpriteCollection):
        width, height = self.get_size(collections)
        left = self.x - width / 2
        bottom = self.y - height / 2
        right = self.x + width / 2
        top = self.y + height / 2

        return left, bottom, right, top
