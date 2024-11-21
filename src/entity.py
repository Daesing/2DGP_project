from animation import SpriteCollection
from animation import SpriteAnimation
from state_machine import StateMachine, AnimationState
from typing import Self


class Entity:

    def __init__(self,x,y,state:AnimationState[Self],width = None,height = None):
        self.current_animation = None
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.animation_time = 0
        self.inverted = False
        self.state_machine = StateMachine(self)
        self.state_machine.start(state)


    def set_animation(self,animation:str, inverted = False):
        self.current_animation = animation
        self.inverted = inverted
        self.animation_time = 0
        print(f'{self.current_animation} inverted: {self.inverted}')

    def draw(self,collections: SpriteCollection):
        animation = collections.get(self.current_animation)
        animation.draw(self.x, self.y, self.animation_time, self.inverted,self.width,self.height)


    def update(self):
        self.animation_time += 0.01

    def get_size(self,collections: SpriteCollection):
        animation = collections.get(self.current_animation)
        width,height = animation.get_size()
        if self.width is not None:
            width = self.width
        if self.height is not None:
            height = self.height

        return width, height


    def get_boundary(self, collections: SpriteCollection):
        width,height = self.get_size(collections)
        left = self.x - width / 2
        bottom = self.y - height / 2
        right = self.x + width / 2
        top = self.y + height / 2

        return left, bottom, right, top
