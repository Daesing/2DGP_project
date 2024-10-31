# event ( 종류 문자열, 실제 값 )
from __future__ import annotations
from sdl2 import SDLK_SPACE, SDL_KEYDOWN, SDLK_RIGHT, SDLK_LEFT, SDL_KEYUP, SDLK_a
from typing import Optional

from src.state_manager import StateManager


def start_event(e):
    return e[0] == 'START'

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT

def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT

def a_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a

def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT

def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def time_out(e):
    return e[0] == 'TIME_OUT'




class AnimationState:
    def on_right_down(self,e) -> Optional[AnimationState]:
        return None

    def on_left_down(self,e) -> Optional[AnimationState]:
        return None

    def on_right_up(self,e) -> Optional[AnimationState]:
        return None

    def on_left_up(self,e) -> Optional[AnimationState]:
        return None

    def on_space_down(self,e) -> Optional[AnimationState]:
        return None

    def on_a_down(self,e) -> Optional[AnimationState]:
        return None

    def on_time_out(self,e) -> Optional[AnimationState]:
        return None

    #state
    def enter(self, knight, e):
        pass

    def exit(self, knight, e):
        pass

    def do(self, knight) -> Optional[AnimationState]:
        return None


events = [
    (left_down, lambda state,e: state.on_left_down(e)),
    (left_up, lambda state,e: state.on_left_up(e)),
    (right_down, lambda state,e: state.on_right_down(e)),
    (right_up, lambda state,e: state.on_right_up(e)),
    (a_down, lambda state,e: state.on_a_down(e)),
    (space_down, lambda state,e: state.on_space_down(e)),
    (time_out, lambda state,e: state.on_time_out(e)),
]

# 상태 머신을 처리 관리해주는 클래스

class StateMachine:
    state_manager:StateManager
    cur_state:AnimationState
    def __init__(self, o):
        self.state_manager = StateManager()
        self.o = o # boy self가 전달, self.o 상태머신과 연결된 캐릭터 객체
        self.event_que = [] # 발생하는 이벤트를 담는

    def update(self):
        next_state = self.cur_state.do(self.o)  # Idle.do()
        self.update_state(next_state, None)

        if not self.event_que:
            return
        # 이벤트 발생했는지 확인하고, 거기에 따라서 상태변환을 수행.
        e = self.event_que.pop(0)   # list의 첫번째 요소를 꺼내
        self.state_manager.on_keyboard_event(e)

        for check_events,perform_action in events:
            if not check_events(e):
                continue
            next_state = perform_action(self.cur_state,e)
            if self.update_state(next_state,e):
                return

    def update_state(self,state,e)->bool:
        if state is None:
            return False
        self.cur_state.exit(self.o, e)
        print(f'Exit from {self.cur_state}')
        self.cur_state = state
        self.cur_state.enter(self.o, e)
        print(f'ENTER into {state}')
        if self.state_manager.jump:
            return self.update_state(self.cur_state.on_space_down(None),None)
        if self.state_manager.right and self.state_manager.left:
            pass
        elif self.state_manager.right:
            return self.update_state(self.cur_state.on_right_down(None),None)
        elif self.state_manager.left:
            return self.update_state(self.cur_state.on_left_down(None),None)

        return True

    def start(self, start_state):
        # 현재 상태를 시작 상태로 만듬.
        self.cur_state = start_state # Idle
        # new start
        self.cur_state.enter(self.o, 'START')
        print(f'ENTER into{self.cur_state}')

    def set_transitions(self, transitions):
        self.set_transitions = transitions
        pass
    def add_event(self, e):
        self.event_que.append(e) # 상태머신용 이벤트 추가
        print(f'    DEBUG new event{e} is added')
        pass