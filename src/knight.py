from src.entity import Entity
from pico2d import *
from state_machine import StateMachine
from state_machine import AnimationState
from typing import Optional


class Idle(AnimationState):

    def __init__(self, direction: str):
        self.direction = direction

    def on_right_down(self):
        return Run('right')

    def on_left_down(self):
        return Run('left')

    def on_right_up(self) -> Optional[AnimationState]:
        if self.direction !='right':
            return Idle('right')
        return None
    def on_left_up(self) -> Optional[AnimationState]:
        if self.direction != 'left':
            return Idle('left')
        return None

    def on_a_down(self) -> Optional[AnimationState]:
        return Slash(self.direction)

    def on_space_down(self) -> Optional[AnimationState]:
        return Jump(self.direction)

    def enter(self, knight):
        if self.direction == 'right':
            knight.current_animation = 'knight_idle_right'
        elif self.direction == 'left':
            knight.current_animation = 'knight_idle_left'

        knight.vx = 0


class Run(AnimationState):

    def __init__(self, direction: str):
        self.direction = direction

    def on_left_up(self) -> Optional[AnimationState]:
        return Idle('left')

    def on_right_up(self) -> Optional[AnimationState]:
        return Idle('right')

    def on_right_down(self) -> Optional[AnimationState]:
        if self.direction != 'right':
            return Run('right')
        return None

    def on_left_down(self) -> Optional[AnimationState]:
        if self.direction != 'left':
            return Run('left')
        return None

    def on_a_down(self) -> Optional[AnimationState]:
        return Slash(self.direction)

    def on_space_down(self) -> Optional[AnimationState]:
        return Jump(self.direction)

    def enter(self, knight):
        if self.direction == 'right':
            knight.vx = 1
            knight.face_dir = 1
            knight.current_animation = 'knight_move_right'
        elif self.direction == 'left':
            knight.vx = -1
            knight.face_dir = -1
            knight.current_animation = 'knight_move_left'


class Slash(AnimationState):
    def __init__(self, direction: str):
        self.direction = direction

    def on_right_down(self) -> Optional[AnimationState]:
        return Run('right')

    def on_left_down(self) -> Optional[AnimationState]:
        return Run('left')

    def on_time_out(self) -> Optional[AnimationState]:
        return Idle(self.direction)

    def enter(self, knight):
        if self.direction == 'right':
            knight.current_animation = 'knight_slash_right'
        elif self.direction == 'left':
            knight.current_animation = 'knight_slash_left'

        knight.start_time = get_time()

    def exit(self, knight):
        pass

    def do(self, knight):
        if get_time() - knight.start_time > 0.7:
            return Idle(self.direction)
        return None


class Jump(AnimationState):
    def __init__(self, direction: str):
        self.direction = direction

    def on_right_down(self) -> Optional[AnimationState]:
        return Run('right')

    def on_left_down(self) -> Optional[AnimationState]:
        return Run('left')

    def on_a_down(self) -> Optional[AnimationState]:
        return Slash(self.direction)

    def on_time_out(self) -> Optional[AnimationState]:
        return Idle(self.direction)

    def enter(self, knight):
        if self.direction == 'right':
            knight.current_animation = 'knight_jump_right'
        elif self.direction == 'left':
            knight.current_animation = 'knight_jump_left'

        knight.start_time = get_time()
        if knight.y == 200:
            knight.vy = 2

    def exit(self, knight):
        pass

    def do(self, knight):
        if knight.y == 200:
            return Idle(self.direction)
        return None


class Knight(Entity):
    def __init__(self, x, y):
        super().__init__()
        self.x, self.y = x, y
        self.vx, self.vy = 0, 0
        self.frame = 0
        self.face_dir = 1
        self.state_machine = StateMachine(self)  # 소년 객체를 위한 상태 머신인지 알려줄 필요
        self.state_machine.start(Idle('right'))  # 객체를 생성한게 아니고, 직접 Idle이라는 클래스를 사용

    def update(self):
        self.state_machine.update()
        self.vy -= 0.01
        self.x += self.vx
        self.y += self.vy
        if self.y < 200:
            self.vy = 0
            self.y = 200

    def handle_event(self, event):
        # event : input event
        # state machine event : (이벤트종류, 값)
        self.state_machine.add_event(
            ('INPUT', event)
        )
