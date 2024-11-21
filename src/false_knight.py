from pico2d import get_time
from entity import Entity
from state_machine import AnimationState


class FalseKnight(Entity):
    start_time: float

    def __init__(self,x,y):
        super().__init__(x, y, Idle('left'), ratio=0.7)
        self.x,y, = x,y

    def update(self):
        super().update()
        self.state_machine.update()

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
            return Idle(self.direction)

        return None



