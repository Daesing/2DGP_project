import threading

from pico2d import load_image, get_time

from entity import Entity
import game_world
from src.animation import SpriteCollection
from state_machine import Delete
from state_machine import AnimationState


PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 1  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

class HornetEffect(Entity):
    start_time: float

    def __init__(self, hornet,direction,action:str):
        self.hornet = hornet
        self.direction = direction
        self.action = action
        self.hit = True    #타 객체와의 중복 충돌을 막는 flag
        if action == 'thread':
            super().__init__(0, 0, Thread())
        elif action == 'needle':
            super().__init__(0, 0, Needle())
        elif action == 'dash':
            super().__init__(0, 0, DashEffect())
        elif action == 'sphere':
            super().__init__(0, 0, SphereEffect())


    def handle_collision(self,group,other):
        if group == 'knight:needle':
            print('needle')
            pass

    def update(self):
        super().update()
        self.state_machine.update()

    def add_effect(self, direction, action):
        effect = HornetEffect(self, direction, action)
        game_world.add_object(effect,2)

class Thread(AnimationState[HornetEffect]):
    def __init__(self):
        pass

    def enter(self, hornet_effect):
        hornet_effect.y = hornet_effect.hornet.y
        print('thread')
        if hornet_effect.direction == 'left':
            hornet_effect.set_animation('hornet_needle_thread')
            hornet_effect.x = hornet_effect.hornet.x - 300

        elif hornet_effect.direction == 'right':
            hornet_effect.set_animation('hornet_needle_thread', True)
            hornet_effect.x = hornet_effect.hornet.x + 300

        hornet_effect.start_time = get_time()

    def do(self, hornet_effect:HornetEffect) -> AnimationState[HornetEffect] | None:
        if get_time() - hornet_effect.start_time > 0.4:
            return Delete()
        return None


    def exit(self,hornet_effect):
        pass

class Needle(AnimationState[HornetEffect]):

    def enter(self, hornet_effect):
        hornet_effect.y = hornet_effect.hornet.y

        if hornet_effect.direction == 'left':
            hornet_effect.set_animation('hornet_needle')
            hornet_effect.x = hornet_effect.hornet.x - 30

        elif hornet_effect.direction == 'right':
            hornet_effect.set_animation('hornet_needle', True)
            hornet_effect.x = hornet_effect.hornet.x + 30

        hornet_effect.start_time = get_time()

    def do(self, hornet_effect:HornetEffect) -> AnimationState[HornetEffect] | None:

        if get_time() - hornet_effect.start_time < 1:
            if hornet_effect.direction == 'left':
                hornet_effect.x -= 2
            elif hornet_effect.direction == 'right':
                hornet_effect.x += 2
        if 1 < get_time() - hornet_effect.start_time < 1.5:
            if hornet_effect.direction == 'left':
                hornet_effect.x += 3
            elif hornet_effect.direction == 'right':
                hornet_effect.x -= 3
        if get_time() - hornet_effect.start_time > 1.5:
            return Delete()

class DashEffect(AnimationState[HornetEffect]):

    def enter(self, hornet_effect):
        hornet_effect.y = hornet_effect.hornet.y+120

        if hornet_effect.direction == 'left':
            hornet_effect.set_animation('hornet_dash_effect')
            hornet_effect.x = hornet_effect.hornet.x + 400

        elif hornet_effect.direction == 'right':
            hornet_effect.set_animation('hornet_dash_effect', True)
            hornet_effect.x = hornet_effect.hornet.x + 400

        hornet_effect.start_time = get_time()

    def do(self, hornet_effect:HornetEffect) -> AnimationState[HornetEffect] | None:
        hornet_effect.y = hornet_effect.hornet.y + 120

        if hornet_effect.direction == 'left':
            hornet_effect.x = hornet_effect.hornet.x + 400

        elif hornet_effect.direction == 'right':
            hornet_effect.x = hornet_effect.hornet.x + 400
        if get_time() - hornet_effect.start_time > 0.5:
            return Delete()

class SphereEffect(AnimationState[HornetEffect]):

    def enter(self, hornet_effect):
        hornet_effect.y = hornet_effect.hornet.y + 50
        hornet_effect.x = hornet_effect.hornet.x

        if hornet_effect.direction == 'left':
            hornet_effect.set_animation('hornet_sphere_effect')


        elif hornet_effect.direction == 'right':
            hornet_effect.set_animation('hornet_sphere_effect', True)

        hornet_effect.start_time = get_time()

    def do(self, hornet_effect:HornetEffect) -> AnimationState[HornetEffect] | None:
        hornet_effect.y = hornet_effect.hornet.y + 50
        hornet_effect.x = hornet_effect.hornet.x

        if get_time() - hornet_effect.start_time > 1.0:
            return Delete()