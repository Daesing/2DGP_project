import random
import threading

from pico2d import *
import game_framework
from entity import Entity
from animation import SpriteCollection
import stage2
from hornet_effect import HornetEffect
import game_world
from header import WIDTH
from state_machine import AnimationState


PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 30  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# 기본 state 방향 = left
class Hornet(Entity):
    start_time: float

    def __init__(self,x,y):
        super().__init__(x, y, PreBarb('left'),ratio=0.7)
        self.audio = None
        self.direction = None
        self.hit = True
        self.x,y, = x,y
        self.ground = y
        self.on_ground = True
        self.vx,self.vy = 0,0
        self.hp = 100
        self.font = load_font('resource/font/ENCR10B.TTF', 16)
        self.state = 'Idle'
        self.dead = False

    def update(self):
        super().update()
        self.state_machine.update()
        self.vy -= 1500 * game_framework.frame_time
        self.x += self.vx * game_framework.frame_time
        self.y += self.vy * game_framework.frame_time
        self.check_action()
        if self.y <= self.ground:
            self.vy = 0
            self.y = self.ground
            self.on_ground = True
        if self.hp == 0:
            self.dead = True

        if self.x < 0:
           self.x = 0
        elif self.x > WIDTH:
            self.x = WIDTH

    def draw(self, collections: SpriteCollection):
        super().draw(collections)
        self.font.draw(self.x, self.y + 100, f'{self.hp:02d}', (255, 255, 0))

    def handle_collision(self,group,other):
        if group == 'knight:hornet':
           pass
        if group == 'slash:hornet' and self.hit:
           if self.hp > 0:
               self.hp -= 5
               self.hit = False
               threading.Timer(0.5, self.reset_hit).start()
        if group == 'fireball:hornet' and self.hit:
           if self.hp > 0:
               self.hp -= 15
               self.hit = False
               threading.Timer(0.5, self.reset_hit).start()

    def reset_hit(self):
        self.hit = True

    def add_effect(self, direction, action):
        effect = HornetEffect(self, direction, action)
        game_world.add_object(effect,2)
        if action == 'needle':
            game_world.add_collision_pair('knight:needle',None,effect)
        elif action == 'barb':
            game_world.add_collision_pair('knight:barb',None,effect)

    def load_audio(self,action):
        if action == 'dash':
            self.audio = load_wav('resource/audio/hornet/hornet_dash.wav')
        elif action =='jump':
            self.audio = load_wav('resource/audio/hornet/hornet_jump.wav')
        elif action == 'land':
            self.audio = load_wav('resource/audio/hornet/hornet_ground_land.wav')
        elif action == 'throw':
            self.audio = load_wav('resource/audio/hornet/hornet_needle_throw_and_return.wav')
        elif action == 'flourish':
            self.audio = load_wav('resource/audio/hornet/Hornet_Fight_Flourish.wav')
        elif action == 'yell1':
            self.audio = load_wav('resource/audio/hornet/Hornet_Fight_Yell_03.wav')
        elif action == 'yell2':
            self.audio = load_wav('resource/audio/hornet/Hornet_Fight_Yell_04.wav')
        self.audio.set_volume(20)
        self.audio.play()

    def check_action(self):


        if stage2.knight.x > self.x:
            self.direction = 'right'
        else:
            self.direction = 'left'

        if abs(stage2.knight.x - self.x) > 300:
            action = random.randint(1, 4)
            if action == 1:
                self.state = 'run'
            elif action == 2:
                self.state = 'jump'
            elif action == 3:
                self.state = 'dash'
            elif action == 4:
                self.state = 'barb'
        else:
            action = random.randint(1, 3)
            if action == 1:
                self.state = 'throw'
            if action == 2:
                self.state = 'flourish'
            if 40 < self.hp < 60:
                self.state = 'stun'

        if self.hp <= 0:
            self.state = 'wounded'



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
        elif hornet.state == 'jump':
            return PreJump(hornet.direction)
        elif hornet.state == 'flourish':
            return Flourish(hornet.direction)
        elif hornet.state == 'dash':
            return PreDash(hornet.direction)
        elif hornet.state == 'stun':
            return Stun(hornet.direction)
        elif hornet.state == 'wounded':
            return Wounded(hornet.direction)
        elif hornet.state == 'barb':
            return PreBarb(hornet.direction)
        return None

class Flourish(AnimationState[Hornet]):
    def __init__(self, direction):
        self.direction = direction

    def enter(self, hornet):
        if self.direction == 'left':
            hornet.set_animation('hornet_flourish')
        elif self.direction == 'right':
            hornet.set_animation('hornet_flourish',True)

        hornet.load_audio('flourish')
        hornet.start_time = get_time()

    def do(self, hornet:Hornet) -> AnimationState[Hornet] | None:
        if get_time() - hornet.start_time > 1.6:

            action = random.randint(1,2)
            if action == 1:
                return PreThrow(self.direction)
            else:
                return Sphere(self.direction)
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

        hornet.load_audio('yell1')
        hornet.start_time = get_time()

    def do(self, hornet: Hornet) -> AnimationState[Hornet] | None:
        if get_time() - hornet.start_time > 0.3:
            if hornet.state == 'jump':
                return Jump(self.direction)
            elif hornet.state == 'sphere':
                return Sphere(self.direction)

        return None


class Jump(AnimationState[Hornet]):
    def __init__(self, direction):
        self.direction = direction

    def enter(self, hornet):
        if self.direction == 'left':
            hornet.vx = - RUN_SPEED_PPS
            hornet.set_animation('hornet_jump')
        elif self.direction == 'right':
            hornet.vx = RUN_SPEED_PPS
            hornet.set_animation('hornet_jump', True)

        hornet.load_audio('jump')
        hornet.start_time = get_time()
        hornet.vy = 1000
        hornet.on_ground = False

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
        if hornet.on_ground:
            hornet.vx = 0

        if get_time() - hornet.start_time > 0.7:
            hornet.load_audio('land')
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

        hornet.load_audio('yell2')
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
        hornet.load_audio('throw')
        hornet.start_time = get_time()

    def do(self, hornet: Hornet) -> AnimationState[Hornet] | None:

        if get_time() - hornet.start_time > 1.0:
            hornet.add_effect(self.direction,'thread')
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

        hornet.start_time = get_time()

    def do(self, hornet: Hornet) -> AnimationState[Hornet] | None:
        if get_time() - hornet.start_time > 0.8:
            return Idle(self.direction)

        return None

class PreDash(AnimationState[Hornet]):
    def __init__(self, direction):
        self.direction = direction

    def enter(self, hornet):
        if self.direction == 'left':
            hornet.set_animation('hornet_dash_pre')
        elif self.direction == 'right':
            hornet.set_animation('hornet_dash_pre', True)

        hornet.load_audio('yell2')
        hornet.start_time = get_time()

    def do(self, hornet: Hornet) -> AnimationState[Hornet] | None:

        if get_time() - hornet.start_time > 0.8:
            return Dash(self.direction)

        return None

class Dash(AnimationState[Hornet]):
    def __init__(self, direction):
        self.direction = direction

    def enter(self, hornet):
        if self.direction == 'left':
            hornet.vx = - RUN_SPEED_PPS * 5
            hornet.set_animation('hornet_dash')
        elif self.direction == 'right':
            hornet.vx = RUN_SPEED_PPS * 5
            hornet.set_animation('hornet_dash', True)

        hornet.add_effect(self.direction,'dash')
        hornet.load_audio('dash')
        hornet.start_time = get_time()

    def do(self, hornet: Hornet) -> AnimationState[Hornet] | None:

        if get_time() - hornet.start_time > 0.3:
            return DashRecover(self.direction)

        return None

class DashRecover(AnimationState[Hornet]):
    def __init__(self, direction):
        self.direction = direction

    def enter(self, hornet):
        hornet.vx = 0

        if self.direction == 'left':
            hornet.set_animation('hornet_dash_recover')
        elif self.direction == 'right':
            hornet.set_animation('hornet_dash_recover', True)

        hornet.start_time = get_time()

    def do(self, hornet: Hornet) -> AnimationState[Hornet] | None:

        if get_time() - hornet.start_time > 1.0:
            return Idle(self.direction)

        return None

class Sphere(AnimationState[Hornet]):
    def __init__(self, direction):
        self.direction = direction

    def enter(self, hornet):

        if self.direction == 'left':
            hornet.set_animation('hornet_sphere')
        elif self.direction == 'right':
            hornet.set_animation('hornet_sphere', True)

        hornet.add_effect(self.direction,'sphere')
        hornet.start_time = get_time()

    def do(self, hornet: Hornet) -> AnimationState[Hornet] | None:
        if get_time() - hornet.start_time > 1.0:
            return SphereRecover(self.direction)

        return None
class SphereRecover(AnimationState[Hornet]):
    def __init__(self, direction):
        self.direction = direction

    def enter(self, hornet):

        if self.direction == 'left':
            hornet.set_animation('hornet_sphere_recover')
        elif self.direction == 'right':
            hornet.set_animation('hornet_sphere_recover', True)

        hornet.start_time = get_time()

    def do(self, hornet: Hornet) -> AnimationState[Hornet] | None:

        if get_time() - hornet.start_time > 0.3:
            return Idle(self.direction)

        return None

class PreBarb(AnimationState[Hornet]):
    def __init__(self, direction):
        self.direction = direction

    def enter(self, hornet):
        if self.direction == 'left':
            hornet.set_animation('hornet_barb_throw_pre')
        elif self.direction == 'right':
            hornet.set_animation('hornet_barb_throw_pre', True)

        hornet.start_time = get_time()

    def do(self, hornet: Hornet) -> AnimationState[Hornet] | None:
        if get_time() - hornet.start_time > 0.5:
            return Barb(self.direction)

        return None

class Barb(AnimationState[Hornet]):
    def __init__(self, direction):
        self.direction = direction

    def enter(self, hornet):
        if self.direction == 'left':
            hornet.set_animation('hornet_barb_throw')
        elif self.direction == 'right':
            hornet.set_animation('hornet_barb_throw', True)

        hornet.start_time = get_time()
        hornet.load_audio('dash')
        hornet.add_effect(self.direction,'barb')

    def do(self, hornet: Hornet) -> AnimationState[Hornet] | None:
        if get_time() - hornet.start_time > 1.0:
            return BarbRecover(self.direction)

        return None

class BarbRecover(AnimationState[Hornet]):
    def __init__(self, direction):
        self.direction = direction

    def enter(self, hornet):
        if self.direction == 'left':
            hornet.set_animation('hornet_barb_throw_recover')
        elif self.direction == 'right':
            hornet.set_animation('hornet_barb_throw_recover', True)

        hornet.start_time = get_time()

    def do(self, hornet: Hornet) -> AnimationState[Hornet] | None:
        if get_time() - hornet.start_time > 0.7:
            return Idle(self.direction)

        return None




class Stun(AnimationState[Hornet]):
    def __init__(self, direction):
        self.direction = direction

    def enter(self, hornet):
        if self.direction == 'left':
            hornet.set_animation('hornet_stun')
        elif self.direction == 'right':
            hornet.set_animation('hornet_stun', True)

    def do(self, hornet: Hornet) -> AnimationState[Hornet] | None:

        if hornet.state != 'stun':
            return Idle(self.direction)

        return None

class Wounded(AnimationState[Hornet]):
    def __init__(self, direction):
        self.direction = direction

    def enter(self, hornet):
        if self.direction == 'left':
            hornet.set_animation('hornet_wounded')
        elif self.direction == 'right':
            hornet.set_animation('hornet_wounded', True)

    def do(self, hornet: Hornet) -> AnimationState[Hornet] | None:

        return None
