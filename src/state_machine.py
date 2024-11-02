# event ( 종류 문자열, 실제 값 )
from __future__ import annotations
from typing import TypeVar

T = TypeVar('T')

class AnimationState[T]:

    #state
    def enter(self, entity:T):
        pass

    def exit(self, entity:T):
        pass

    def do(self, entity:T) -> AnimationState[T] | None:
        return None



# 상태 머신을 처리 관리해주는 클래스

class StateMachine[T]:
    cur_state:AnimationState[T]
    def __init__(self, o):
        self.o = o # boy self가 전달, self.o 상태머신과 연결된 캐릭터 객체

    def update(self):
        next_state = self.cur_state.do(self.o)  # Idle.do()
        if next_state is None:
            return False
        self.cur_state.exit(self.o)
        print(f'Exit from {self.cur_state}')
        self.cur_state = next_state
        self.cur_state.enter(self.o)
        print(f'ENTER into {next_state}')

        return True


    def start(self, start_state):
        # 현재 상태를 시작 상태로 만듬.
        self.cur_state = start_state # Idle
        # new start
        self.cur_state.enter(self.o)
        print(f'ENTER into{self.cur_state}')

    def set_transitions(self, transitions):
        self.transitions = transitions
