from bdb import effective

from entity import Entity
from pico2d import *
from input_manager import InputManager
from knight_effect import KnightEffect
import game_world
import game_framework
from state_machine import AnimationState

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 40.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

class Knight(Entity):
    start_time: float

    def __init__(self, x, y):
        super().__init__(x, y, Idle('right'))
        self.vx, self.vy = 0, 0
        self.ground = y
        self.on_ground = True
        self.input_manager = InputManager()

    # boy.x += boy.dir * RUN_SPEED_PPS * game_framework.frame_time
    def update(self):
        super().update()
        self.state_machine.update()
        self.vy -= 1500 * game_framework.frame_time
        self.x += self.vx * game_framework.frame_time
        self.y += self.vy * game_framework.frame_time
        if self.y <= self.ground:
            self.vy = 0
            self.y = self.ground
            self.on_ground = True

    def handle_event(self, event: Event):
        self.input_manager.on_keyboard_event(event)

    def update_effect(self,direction):
        effect = KnightEffect(self,direction)
        game_world.add_object(effect,2)


class Idle(AnimationState[Knight]):

    def __init__(self, direction: str):
        self.direction = direction

    def enter(self, knight):
        if self.direction == 'right':
            knight.set_animation('knight_idle_right')
        elif self.direction == 'left':
            knight.set_animation('knight_idle_left')

        knight.vx = 0

    def do(self, entity: Knight) -> AnimationState[Knight] | None:
        if entity.input_manager.jump: return Jump(self.direction)
        if entity.input_manager.slash: return Slash(self.direction)

        if entity.input_manager.left and entity.input_manager.right:
            pass
        elif entity.input_manager.left:
            return Run('left')
        elif entity.input_manager.right:
            return Run('right')

        return None


class Run(AnimationState[Knight]):

    def __init__(self, direction: str):
        self.direction = direction


    def enter(self, knight):
        if self.direction == 'right':
            knight.vx = RUN_SPEED_PPS
            knight.set_animation('knight_move_right')

        elif self.direction == 'left':
            knight.vx = - RUN_SPEED_PPS
            knight.set_animation('knight_move_left')

    def exit(self,knight):
        pass

    def do(self, entity: Knight) -> AnimationState[Knight] | None:
        if entity.input_manager.jump: return Jump(self.direction)
        if entity.input_manager.slash:
            return Slash(self.direction)

        if entity.input_manager.left and entity.input_manager.right:
            return Idle(self.direction)
        elif entity.input_manager.left:
            if self.direction == 'right':
                return Run('left')
            else:
                return None
        elif entity.input_manager.right:
            if self.direction == 'left':
                return Run('right')
            else:
                return None

        return Idle(self.direction)


class Slash(AnimationState):
    def __init__(self, direction: str):
        self.direction = direction

    def enter(self, knight):
        print('slash enter')
        if self.direction == 'right':
            knight.set_animation('knight_slash_right')
        elif self.direction == 'left':
            knight.set_animation('knight_slash_left')

        knight.update_effect(self.direction)
        knight.start_time = get_time()


    def exit(self, knight):
        pass

    def do(self, entity: Knight) -> AnimationState[Knight] | None:
        if entity.input_manager.jump:
            return Jump(self.direction)
        if get_time() - entity.start_time > 0.7:
            if not entity.on_ground:
                return OnAir(self.direction)

            if entity.input_manager.left and entity.input_manager.right:
                return Idle(self.direction)
            elif entity.input_manager.left:
                return Run('left')
            elif entity.input_manager.right:
                return Run('right')

            return Idle(self.direction)
        return None


class Jump(AnimationState):
    def __init__(self, direction: str):
        self.start_time = None
        self.direction = direction

    def enter(self, knight):
        if self.direction == 'right':
            knight.set_animation('knight_jump_right')
            knight.vx = RUN_SPEED_PPS
        elif self.direction == 'left':
            knight.set_animation('knight_jump_left')
            knight.vx = - RUN_SPEED_PPS
        self.start_time = get_time()

        if knight.on_ground:
            knight.vy = 700
            knight.on_ground = False

    def exit(self, knight):
        pass

    def do(self, entity: Knight) -> AnimationState[Knight] | None:
        if entity.on_ground:
            return Idle(self.direction)
        if get_time() - self.start_time > 0.7:
            return OnAir(self.direction)
        if entity.input_manager.slash:
            return Slash(self.direction)

        if entity.input_manager.left and entity.input_manager.right:
            entity.vx = 0
        elif entity.input_manager.left:
            return OnAir('left')
        elif entity.input_manager.right:
            return OnAir('right')
        else:
            entity.vx = 0

        return None


class OnAir(AnimationState[Knight]):
    direction: str

    def __init__(self, direction: str):
        self.direction = direction

    def enter(self, knight):
        # todo: Knight_jump_right를 Knight_on_air_right로 바꿀 것
        if self.direction == 'right':
            knight.vx = RUN_SPEED_PPS
            knight.set_animation('knight_jump_right')
        # todo: Knight_jump_left를 Knight_on_air_left로 바꿀 것
        elif self.direction == 'left':
            knight.set_animation('knight_jump_left')
            knight.vx = - RUN_SPEED_PPS

    def do(self, entity: Knight) -> AnimationState[Knight] | None:
        if entity.on_ground:
            return Idle(self.direction)
        if entity.input_manager.slash: return Slash(self.direction)
        if entity.input_manager.left and entity.input_manager.right:
            entity.vx = 0
        elif entity.input_manager.left:
            entity.vx = -RUN_SPEED_PPS
            if self.direction == 'right':
                return OnAir('left')
        elif entity.input_manager.right:
            entity.vx = RUN_SPEED_PPS
            if self.direction == 'left':
                return OnAir('right')
        else:
            entity.vx = 0
        return None
