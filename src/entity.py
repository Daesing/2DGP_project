from animation import SpriteCollection
from src.state_machine import StateMachine, AnimationState
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

    def draw_animation(self,collections: SpriteCollection):
        collections.get(self.current_animation).draw(self.x, self.y, self.animation_time)


    def update_time(self, delta_time):
        self.animation_time += delta_time
        self.update()

    def update(self):
        pass



