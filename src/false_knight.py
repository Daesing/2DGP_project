from pico2d import get_time
from entity import Entity
import game_framework
from state_machine import AnimationState

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 30.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)


class FalseKnight(Entity):
    start_time: float

    def __init__(self,x,y):
        super().__init__(x, y, PreJump('left'), ratio=0.7)
        self.x,y, = x,y
        self.ground = y
        self.on_ground = True
        self.vx,self.vy = 0,0

    def update(self):
        super().update()
        self.state_machine.update()
        self.vy -= 1500 * game_framework.frame_time
        self.x += self.vx * game_framework.frame_time
        self.y += self.vy * game_framework.frame_time
        if self.y <= self.ground:
            self.vy = 0
            self.y = self.ground

    def handle_collision(self,group,other):
        if group == 'slash:false_knight':
            pass

class Idle(AnimationState[FalseKnight]):
    def __init__(self,direction):
        self.direction = direction

    def enter(self, false_knight):
        if self.direction == 'left':
            false_knight.set_animation('false_knight_idle', True)
        if self.direction == 'right':
            false_knight.set_animation('false_knight_idle')

        false_knight.start_time = get_time()

    def do(self, false_knight:FalseKnight) -> AnimationState[FalseKnight] | None:

        if get_time() - false_knight.start_time > 2:
            return PreRun(self.direction)

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
        elif self.direction == 'right':
            false_knight.set_animation('false_knight_run')

        false_knight.start_time = get_time()

    def do(self, false_knight:FalseKnight) -> AnimationState[FalseKnight] | None:


        if get_time() - false_knight.start_time > 2:
            return PreJump(self.direction)

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

        false_knight.vy = 1000
        false_knight.on_ground = False
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
            return Idle(self.direction)

        return None



