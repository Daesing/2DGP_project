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
        self.inverted = False

    def set_animation(self,animation:str,inverted = False):
        self.current_animation = animation
        self.inverted = inverted
        self.animation_time = 0

    def draw(self,collections: SpriteCollection):
        pass


    def update(self):
        self.animation_time += 0.01



