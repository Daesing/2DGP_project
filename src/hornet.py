import random

from pico2d import *
import game_framework
from entity import Entity
from animation import SpriteCollection
import stage2
from hornet_effect import HornetEffect
import game_world
from state_machine import AnimationState


PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# 기본 state 방향 = left
class Hornet(Entity):
    start_time: float

    def __init__(self,x,y):
        super().__init__(x, y, Idle('left'), ratio=0.7)
        self.direction = None
        self.hit = True
        self.x,y, = x,y
        self.ground = y
        self.on_ground = True
        self.vx,self.vy = 0,0
        self.hp = 100
        self.font = load_font('../resource/font/ENCR10B.TTF', 16)
        self.state = 'Idle'
        self.dead = False

    def update(self):
        super().update()
        self.state_machine.update()
        self.vy -= 1500 * game_framework.frame_time
        self.x += self.vx * game_framework.frame_time
        self.y += self.vy * game_framework.frame_time
        self.check_run()
        if self.y <= self.ground:
            self.vy = 0
            self.y = self.ground
        if self.hp == 0:
            self.dead = True

    def draw(self, collections: SpriteCollection):
        super().draw(collections)
        self.font.draw(self.x, self.y + 300, f'{self.hp:02d}', (255, 255, 0))

    def handle_collision(self,group,other):
       pass

    def reset_hit(self):
        self.hit = True

    def add_effect(self, direction, action):
        effect = HornetEffect(self, direction, action)
        game_world.add_object(effect,2)

    def check_run(self):
        if stage2.knight.x > self.x:
            self.direction = 'right'
        else:
            self.direction = 'left'

        if abs(stage2.knight.x - self.x) > 300:
            self.state = 'run'
        else:
            action = random.randint(1, 3)
            if action == 1:
                self.state = 'throw'

class Idle(AnimationState[Hornet]):

    def __init__(self, direction):
        self.direction = direction

    def enter(self,hornet):
        if self.direction == 'left':
            hornet.set_animation('hornet_idle')
        elif self.direction == 'right':
            hornet.set_animation('hornet_idle',True)

        hornet.vx = 0
        hornet.start_time = get_time()

    def do(self, hornet:Hornet) -> AnimationState[Hornet] | None:
        if hornet.state == 'run':
            return Run(hornet.direction)
        elif hornet.state == 'throw':
            return PreThrow(hornet.direction)
        return None

class Flourish(AnimationState[Hornet]):
    def __init__(self, direction):
        self.direction = direction

    def enter(self, hornet):
        if self.direction == 'left':
            hornet.set_animation('hornet_flourish')
        elif self.direction == 'right':
            hornet.set_animation('hornet_flourish',True)

        hornet.start_time = get_time()

    def do(self, hornet:Hornet) -> AnimationState[Hornet] | None:
        if get_time() - hornet.start_time > 3:
            return Idle(self.direction)
        return None

class Run(AnimationState[Hornet]):
    def __init__(self,direction):
        self.direction = direction

    def enter(self, hornet):
        if self.direction == 'left':
            hornet.set_animation('hornet_run')
            hornet.vx = - RUN_SPEED_PPS
        elif self.direction == 'right':
            hornet.set_animation('hornet_run', True)
            hornet.vx = RUN_SPEED_PPS

        hornet.start_time = get_time()

    def do(self, hornet:Hornet) -> AnimationState[Hornet] | None:
        if get_time() - hornet.start_time > 0.7:
            hornet.state = 'idle'
            return Idle(self.direction)

        return None


class PreJump(AnimationState[Hornet]):
    def __init__(self, direction):
        self.direction = direction

    def enter(self, hornet):
        if self.direction == 'left':
            hornet.set_animation('hornet_jump_pre')
        elif self.direction == 'right':
            hornet.set_animation('hornet_jump_pre', True)

        hornet.start_time = get_time()

    def do(self, hornet: Hornet) -> AnimationState[Hornet] | None:
        if get_time() - hornet.start_time > 0.3:
            return Jump(self.direction)

        return None


class Jump(AnimationState[Hornet]):
    def __init__(self, direction):
        self.direction = direction

    def enter(self, hornet):
        if self.direction == 'left':
            hornet.set_animation('hornet_jump')
        elif self.direction == 'right':
            hornet.set_animation('hornet_jump', True)

        hornet.start_time = get_time()
        hornet.vy = 1000

    def do(self, hornet: Hornet) -> AnimationState[Hornet] | None:
        if get_time() - hornet.start_time > 1:
            return Land(self.direction)

        return None

class Land(AnimationState[Hornet]):
    def __init__(self, direction):
        self.direction = direction

    def enter(self, hornet):
        if self.direction == 'left':
            hornet.set_animation('hornet_land')
        elif self.direction == 'right':
            hornet.set_animation('hornet_land', True)

        hornet.start_time = get_time()

    def do(self, hornet: Hornet) -> AnimationState[Hornet] | None:
        if get_time() - hornet.start_time > 0.7:
            return Idle(self.direction)

        return None

class PreThrow(AnimationState[Hornet]):
    def __init__(self, direction):
        self.direction = direction

    def enter(self, hornet):
        if self.direction == 'left':
            hornet.set_animation('hornet_throw_pre')
        elif self.direction == 'right':
            hornet.set_animation('hornet_throw_pre', True)

        hornet.start_time = get_time()

    def do(self, hornet: Hornet) -> AnimationState[Hornet] | None:
        if get_time() - hornet.start_time > 0.8:
            return Throw(self.direction)

        return None

class Throw(AnimationState[Hornet]):
    def __init__(self, direction):
        self.direction = direction

    def enter(self, hornet):
        if self.direction == 'left':
            hornet.set_animation('hornet_throw')
        elif self.direction == 'right':
            hornet.set_animation('hornet_throw', True)

        hornet.add_effect(self.direction,'needle')
        hornet.start_time = get_time()

    def do(self, hornet: Hornet) -> AnimationState[Hornet] | None:
        if get_time() - hornet.start_time > 1.0:
            return ThrowRecover(self.direction)

        return None

class ThrowRecover(AnimationState[Hornet]):
    def __init__(self, direction):
        self.direction = direction

    def enter(self, hornet):
        if self.direction == 'left':
            hornet.set_animation('hornet_throw_recover')
        elif self.direction == 'right':
            hornet.set_animation('hornet_throw_recover', True)

        hornet.add_effect(self.direction, 'thread')
        hornet.start_time = get_time()

    def do(self, hornet: Hornet) -> AnimationState[Hornet] | None:
        if get_time() - hornet.start_time > 0.8:
            return Idle(self.direction)

        return None


