from entity import Entity
from pico2d import *
from input_manager import InputManager
from state_machine import AnimationState


class Knight(Entity):
    start_time: float

    def __init__(self, x=300, y=200):
        super().__init__(x,y,Idle('right'))
        self.vx, self.vy = 0, 0
        self.on_ground = True
        self.input_manager = InputManager()

    def update(self):
        self.state_machine.update()
        self.vy -= 0.01
        self.x += self.vx
        self.y += self.vy
        if self.y <= 200:
            self.vy = 0
            self.y = 200
            self.on_ground = True

    def handle_event(self, event: Event):
        # event : input event
        # state machine event : (이벤트종류, 값)
        self.input_manager.on_keyboard_event(event)


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
            knight.vx = 1
            knight.face_dir = 1
            knight.set_animation('knight_move_right')
        elif self.direction == 'left':
            knight.vx = -1
            knight.face_dir = -1
            knight.set_animation('knight_move_left')

    def do(self, entity: Knight) -> AnimationState[Knight] | None:
        if entity.input_manager.jump: return Jump(self.direction)
        if entity.input_manager.slash: return Slash(self.direction)

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
        if self.direction == 'right':
            knight.set_animation('knight_slash_right')
        elif self.direction == 'left':
            knight.set_animation('knight_slash_left')

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
            knight.vx = 1
        elif self.direction == 'left':
            knight.set_animation('knight_jump_left')
            knight.vx = -1
        self.start_time = get_time()

        if knight.on_ground:
            knight.vy = 2
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
            knight.vx = 1
            knight.set_animation('knight_jump_right')
        # todo: Knight_jump_left를 Knight_on_air_left로 바꿀 것
        elif self.direction == 'left':
            knight.set_animation('knight_jump_left')
            knight.vx = -1

    def do(self, entity: Knight) -> AnimationState[Knight] | None:
        if entity.on_ground:
            return Idle(self.direction)
        if entity.input_manager.slash: return Slash(self.direction)
        if entity.input_manager.left and entity.input_manager.right:
            entity.vx = 0
        elif entity.input_manager.left:
            entity.vx = -1
            if self.direction == 'right':
                return OnAir('left')
        elif entity.input_manager.right:
            entity.vx = 1
            if self.direction == 'left':
                return OnAir('right')
        else:
            entity.vx = 0
        return None
