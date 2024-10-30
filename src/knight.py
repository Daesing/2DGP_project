from src.entity import Entity
from pico2d import *

from src.state_machine import space_down
from state_machine import StateMachine,  time_out, right_down, left_down, right_up, left_up, a_down


class Idle:
    @staticmethod
    def enter(knight, e):
        if right_up(e) or left_down(e):
            knight.current_animation = 'knight_idle_right'
        elif left_up(e) or right_down(e):
            knight.current_animation = 'knight_idle_left'

        knight.vx = 0

        pass

    @staticmethod
    def exit(knight, e):
        pass

    @staticmethod
    def do(knight):
        pass

class Run:
    @staticmethod
    def enter(knight, e):
        if right_down(e) or left_up(e):
            knight.vx = 1
            knight.face_dir = 1
            knight.current_animation = 'knight_move_right'
        elif left_down(e) or right_up(e):
            knight.vx = -1
            knight.face_dir = -1
            knight.current_animation = 'knight_move_left'

        pass

    @staticmethod
    def exit(knight, e):
        pass

    @staticmethod
    def do(knight):
        pass

class Slash:
    @staticmethod
    def enter(knight,e):
        if knight.face_dir == 1:
            knight.current_animation = 'knight_slash_right'
        elif knight.face_dir == -1:
            knight.current_animation = 'knight_slash_left'

        knight.start_time = get_time()
        pass
    @staticmethod
    def exit(knight,e):
        if knight.face_dir == 1:
            knight.current_animation = 'knight_idle_right'
        elif knight.face_dir == -1:
            knight.current_animation = 'knight_idle_left'
        pass
    @staticmethod
    def do(knight):
        if get_time() - knight.start_time > 1:
            # 이벤트를 발생
            knight.state_machine.add_event(('Time_OUT', 0))
        pass


class Jump:
    @staticmethod
    def enter(knight, e):
        knight.current_animation = 'knight_jump'
        knight.start_time = get_time()
        knight.vy = 2
        pass

    @staticmethod
    def exit(knight, e):
        if knight.face_dir == 1:
            knight.current_animation = 'knight_idle_right'
        elif knight.face_dir == -1:
            knight.current_animation = 'knight_idle_left'
        pass

    @staticmethod
    def do(knight):
        if knight.y == 200:
            # 이벤트를 발생
            knight.state_machine.add_event(('Time_OUT', 0))
        pass



class Knight(Entity):
    def __init__(self,x,y):
        super().__init__()
        self.x, self.y = x,y
        self.vx,self.vy = 0, 0
        self.frame = 0
        self.face_dir = 1
        self.state_machine = StateMachine(self)  # 소년 객체를 위한 상태 머신인지 알려줄 필요
        self.state_machine.start(Idle)  # 객체를 생성한게 아니고, 직접 Idle이라는 클래스를 사용
        self.state_machine.set_transitions(
            {
                Idle: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, a_down: Slash, space_down: Jump},
                Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, a_down: Slash,
                      space_down: Jump},
                Slash: {right_down: Run, left_down: Run, time_out: Idle},
                Jump: {time_out: Idle, right_down: Run, left_down: Run, right_up: Idle, left_up: Idle},


            }
        )

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

