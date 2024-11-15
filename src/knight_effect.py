from pico2d import load_image, get_time

from entity import Entity
import game_world
from state_machine import AnimationState


class KnightEffect(Entity):
    start_time: float

    def __init__(self, x, y, direction):
        super().__init__(x, y, Slash(direction))
        self.x, self.y = x,y
        self.direction = direction


    def update(self):
        super().update()
        self.state_machine.update()

class Idle(AnimationState[KnightEffect]):
    def __init__(self,direction):
        self.direction = direction
    def enter(self,knight_effect):
        knight_effect.direction = None

    def do(self, entity:KnightEffect) -> AnimationState[KnightEffect] | None:
        if entity.direction is not None:
            return Slash(self.direction)
        return None

    def exit(self,knight_effect):
        pass

class Slash(AnimationState[KnightEffect]):
    def __init__(self,direction: str):
        self.direction = direction

    def enter(self, knight_effect):
        print('Slash effect enter')
        if self.direction == 'left':
            knight_effect.set_animation = 'knight_slash_effect_left'
        elif self.direction == 'right':
            knight_effect.set_animation = 'knight_slash_effect_right'

        knight_effect.start_time = get_time()

    def do(self, entity:KnightEffect) -> AnimationState[KnightEffect] | None:
        if entity.start_time > 0.5:
            return Idle(self.direction)
        return None


    def exit(self,knight_effect):
        pass
