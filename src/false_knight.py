import random
import threading

from pico2d import get_time, load_font, load_wav
from entity import Entity
import game_framework
import stage1
from animation import SpriteCollection
from state_machine import AnimationState

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 40.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)


class FalseKnight(Entity):
    start_time: float

    def __init__(self,x,y):
        super().__init__(x, y, Idle('left'), ratio=0.7)
        self.direction = None
        self.hit = True
        self.x,y, = x,y
        self.ground = y
        self.on_ground = True
        self.vx,self.vy = 0,0
        self.hp = 200
        self.font = load_font('../resource/font/ENCR10B.TTF', 16)
        self.state = 'Idle'
        self.dead = False
        self.audio = None

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
        if self.hp <= 0:
            self.dead = True

    def draw(self, collections: SpriteCollection):
        super().draw(collections)
        self.font.draw(self.x, self.y + 300, f'{self.hp:02d}', (255, 255, 0))

    def handle_collision(self,group,other):
        if group == 'slash:false_knight' and self.hit:
            if self.hp > 0:
                self.hp -= 5
                self.hit = False
                threading.Timer(0.5,self.reset_hit).start()
        if group == 'fireball:false_knight'and self.hit:
            if self.hp > 0:
                self.hp -= 15
                self.hit = False
                threading.Timer(0.5, self.reset_hit).start()
    def reset_hit(self):
        self.hit = True

    def check_run(self):
        if stage1.knight.x > self.x:
            self.direction = 'right'
        else:
            self.direction = 'left'

        if abs(stage1.knight.x - self.x) > 400:
            self.state = 'run'
        else:
            action = random.randint(1,3)
            if action == 1:
                self.state = 'jump_attack'
            elif action == 2:
                self.state = 'jump'
            else:
                self.state = 'attack'

            if 40 < self.hp < 60:
                self.state = 'stun'

        if self.hp <= 0:
            self.state = 'death'



    def load_audio(self,action:str):
        if action == 'jump':
            self.audio = load_wav('../resource/audio/false_knight/false_knight_jump.wav')
        elif action == 'land':
            self.audio = load_wav('../resource/audio/false_knight/false_knight_land.wav')
        elif action == 'swing':
            self.audio = load_wav('../resource/audio/false_knight/false_knight_swing.wav')
        elif action == 'strike':
            self.audio = load_wav('../resource/audio/false_knight/false_knight_strike_ground.wav')
        self.audio.set_volume(20)
        self.audio.play()

class Idle(AnimationState[FalseKnight]):
    def __init__(self,direction):
        self.direction = direction

    def enter(self, false_knight):
        if self.direction == 'left':
            false_knight.set_animation('false_knight_idle', True)
        if self.direction == 'right':
            false_knight.set_animation('false_knight_idle')

        false_knight.vx = 0
        false_knight.start_time = get_time()

    def do(self, false_knight:FalseKnight) -> AnimationState[FalseKnight] | None:

        if false_knight.state == 'run':
            return PreRun(false_knight.direction)
        elif false_knight.state == 'attack':
            return PreAttack(false_knight.direction)
        elif false_knight.state == 'jump_attack':
            return PreJump(false_knight.direction)
        elif false_knight.state == 'jump':
            return PreJump(false_knight.direction)
        elif false_knight.state == 'death':
            return PreStun(false_knight.direction)
        elif false_knight.state == 'stun':
            return PreStun(false_knight.direction)

        return None

class PreRun(AnimationState[FalseKnight]):
    def __init__(self,direction):
        self.direction = direction

    def enter(self, false_knight):
        if self.direction == 'left':
            false_knight.set_animation('false_knight_run_pre',True)
        elif self.direction == 'right':
            false_knight.set_animation('false_knight_run_pre')

            false_knight.start_time = get_time()

    def do(self, false_knight:FalseKnight) -> AnimationState[FalseKnight] | None:

        if get_time() - false_knight.start_time > 2:
            return Run(self.direction)

        return None

class Run(AnimationState[FalseKnight]):
    def __init__(self,direction):
        self.direction = direction

    def enter(self,false_knight):
        if self.direction == 'left':
            false_knight.set_animation('false_knight_run',True)
            false_knight.vx = - RUN_SPEED_PPS
        elif self.direction == 'right':
            false_knight.set_animation('false_knight_run')
            false_knight.vx = RUN_SPEED_PPS

        false_knight.start_time = get_time()

    def do(self, false_knight:FalseKnight) -> AnimationState[FalseKnight] | None:


        if get_time() - false_knight.start_time > 1.0:
            false_knight.state = 'Idle'
            return Idle(self.direction)

        return None

class PreJump(AnimationState[FalseKnight]):
    def __init__(self,direction):
        self.direction = direction

    def enter(self,false_knight):
        if self.direction == 'left':
            false_knight.set_animation('false_knight_jump_pre',True)
        elif self.direction == 'right':
            false_knight.set_animation('false_knight_jump_pre')

        false_knight.start_time = get_time()

    def do(self, false_knight:FalseKnight) -> AnimationState[FalseKnight] | None:
        if get_time() - false_knight.start_time > 0.5:
            if false_knight.state == 'jump_attack':
                return JumpAttackUp(self.direction)
            elif false_knight.state == 'jump':
                return Jump(self.direction)

        return None

class Jump(AnimationState[FalseKnight]):
    def __init__(self, direction):
        self.direction = direction

    def enter(self, false_knight):
        if self.direction == 'left':
            false_knight.set_animation('false_knight_jump', True)
        elif self.direction == 'right':
            false_knight.set_animation('false_knight_jump')

        false_knight.vy = 1300
        false_knight.on_ground = False
        false_knight.load_audio('jump')
        false_knight.start_time = get_time()

    def do(self, false_knight: FalseKnight) -> AnimationState[FalseKnight] | None:
        if get_time() - false_knight.start_time > 1.1:
            return Land(self.direction)

        return None

class Land(AnimationState[FalseKnight]):
    def __init__(self, direction):
        self.direction = direction

    def enter(self, false_knight):
        if self.direction == 'left':
            false_knight.set_animation('false_knight_land', True)
        elif self.direction == 'right':
            false_knight.set_animation('false_knight_land')


        false_knight.start_time = get_time()

    def do(self, false_knight: FalseKnight) -> AnimationState[FalseKnight] | None:

        if get_time() - false_knight.start_time > 1.0:
            false_knight.load_audio('land')
            return Idle(self.direction)

        return None


class PreAttack(AnimationState[FalseKnight]):
    def __init__(self, direction):
        self.direction = direction

    def enter(self, false_knight):
        if self.direction == 'left':
            false_knight.set_animation('false_knight_attack_pre', True)
        elif self.direction == 'right':
            false_knight.set_animation('false_knight_attack_pre')

        false_knight.start_time = get_time()

    def do(self, false_knight: FalseKnight) -> AnimationState[FalseKnight] | None:
        if get_time() - false_knight.start_time > 0.5:
            return Attack(self.direction)

        return None


class Attack(AnimationState[FalseKnight]):
    def __init__(self, direction):
        self.direction = direction

    def enter(self, false_knight):
        if self.direction == 'left':
            false_knight.set_animation('false_knight_attack', True)
        elif self.direction == 'right':
            false_knight.set_animation('false_knight_attack')

        false_knight.load_audio('swing')
        false_knight.start_time = get_time()

    def do(self, false_knight: FalseKnight) -> AnimationState[FalseKnight] | None:
        if get_time() - false_knight.start_time > 0.7:
            false_knight.load_audio('strike')
            return Recover(self.direction)

        return None

class Recover(AnimationState[FalseKnight]):
    def __init__(self, direction):
        self.direction = direction

    def enter(self, false_knight):
        if self.direction == 'left':
            false_knight.set_animation('false_knight_recover', True)
        elif self.direction == 'right':
            false_knight.set_animation('false_knight_recover')

        false_knight.start_time = get_time()

    def do(self, false_knight: FalseKnight) -> AnimationState[FalseKnight] | None:
        if get_time() - false_knight.start_time > 0.8:
            return Idle(self.direction)

        return None

class JumpAttackUp(AnimationState[FalseKnight]):
    def __init__(self, direction):
        self.direction = direction

    def enter(self, false_knight):
        if self.direction == 'left':
            false_knight.set_animation('false_knight_jump_attack_up', True)
        elif self.direction == 'right':
            false_knight.set_animation('false_knight_jump_attack_up')

        false_knight.vy = 1000
        false_knight.on_ground = False
        false_knight.start_time = get_time()

    def do(self, false_knight: FalseKnight) -> AnimationState[FalseKnight] | None:
        if get_time() - false_knight.start_time > 0.8:
            return JumpAttack1(self.direction)

        return None

class JumpAttack1(AnimationState[FalseKnight]):
    def __init__(self, direction):
        self.direction = direction

    def enter(self, false_knight):
        if self.direction == 'left':
            false_knight.set_animation('false_knight_jump_attack1', True)
        elif self.direction == 'right':
            false_knight.set_animation('false_knight_jump_attack1')

        false_knight.load_audio('swing')
        false_knight.start_time = get_time()

    def do(self, false_knight: FalseKnight) -> AnimationState[FalseKnight] | None:
        if get_time() - false_knight.start_time > 1.0:
            false_knight.load_audio('strike')
            return JumpAttack2(self.direction)

        return None
class JumpAttack2(AnimationState[FalseKnight]):
    def __init__(self, direction):
        self.direction = direction

    def enter(self, false_knight):
        if self.direction == 'left':
            false_knight.set_animation('false_knight_jump_attack2', True)
        elif self.direction == 'right':
            false_knight.set_animation('false_knight_jump_attack2')

        false_knight.start_time = get_time()

    def do(self, false_knight: FalseKnight) -> AnimationState[FalseKnight] | None:
        if get_time() - false_knight.start_time > 0.2:
            return JumpAttack3(self.direction)

        return None

class JumpAttack3(AnimationState[FalseKnight]):
    def __init__(self, direction):
        self.direction = direction

    def enter(self, false_knight):
        if self.direction == 'left':
            false_knight.set_animation('false_knight_jump_attack3', True)
        elif self.direction == 'right':
            false_knight.set_animation('false_knight_jump_attack3')

        false_knight.load_audio('land')
        false_knight.start_time = get_time()

    def do(self, false_knight: FalseKnight) -> AnimationState[FalseKnight] | None:
        if get_time() - false_knight.start_time > 0.5:
            return Idle(self.direction)

        return None

class PreStun(AnimationState[FalseKnight]):
    def __init__(self, direction):
        self.direction = direction

    def enter(self, false_knight):
        if self.direction == 'left':
            false_knight.set_animation('false_knight_stun_pre', True)
        elif self.direction == 'right':
            false_knight.set_animation('false_knight_stun_pre')

        false_knight.start_time = get_time()

    def do(self, false_knight: FalseKnight) -> AnimationState[FalseKnight] | None:
        if get_time() - false_knight.start_time > 0.5:
            if false_knight.state == 'stun':
                return Stun(self.direction)
            elif false_knight.state == 'death':
                return Death(self.direction)
        return None


class Stun(AnimationState[FalseKnight]):
    def __init__(self, direction):
        self.direction = direction

    def enter(self, false_knight):
        if self.direction == 'left':
            false_knight.set_animation('false_knight_stun', True)
        elif self.direction == 'right':
            false_knight.set_animation('false_knight_stun')

    def do(self, false_knight: FalseKnight) -> AnimationState[FalseKnight] | None:
        if false_knight.state != 'stun':
            return Idle(self.direction)

        return None


class Death(AnimationState[FalseKnight]):
    def __init__(self, direction):
        self.direction = direction

    def enter(self, false_knight):
        if self.direction == 'left':
            false_knight.set_animation('false_knight_death', True)
        elif self.direction == 'right':
            false_knight.set_animation('false_knight_death')

    def do(self, false_knight: FalseKnight) -> AnimationState[FalseKnight] | None:

        return None

