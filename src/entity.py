from animation import SpriteCollection
from animation import SpriteAnimation
from state_machine import StateMachine, AnimationState
from typing import Self


class Entity:

    def __init__(self,x,y,state:AnimationState[Self]):
        self.current_animation = None
        self.x = x
        self.y = y
        self.animation_time = 0
        self.state_machine = StateMachine(self)
        self.state_machine.start(state)

    def set_animation(self,animation:str):
        self.current_animation = animation
        self.animation_time = 0

    def draw(self,collections: SpriteCollection):
        pass

    def get_boundary(self,collections: SpriteCollection):
        width,height = collections.get(self.current_animation).get_size()

        left = self.x - width / 2
        bottom = self.y - height / 2
        right = self.x + width / 2
        top = self.y + height / 2

        return left, bottom, right, top

    def update(self):
        self.animation_time += 0.01



