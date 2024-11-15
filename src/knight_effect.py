from pico2d import load_image, get_time

from entity import Entity
from state_machine import Delete
from state_machine import AnimationState


class KnightEffect(Entity):
    start_time: float

    def __init__(self, knight,direction):
        self.knight = knight
        self.direction = direction
        super().__init__(0, 0, Slash())


    def update(self):
        super().update()
        self.state_machine.update()

class Slash(AnimationState[KnightEffect]):
    def __init__(self):
        pass

    def enter(self, knight_effect):
        print('Slash effect enter')
        if knight_effect.direction == 'left':
            knight_effect.set_animation('knight_slash_effect_left')
            knight_effect.x = knight_effect.knight.x - 70
        elif knight_effect.direction == 'right':
            knight_effect.set_animation('knight_slash_effect_right')
            knight_effect.x = knight_effect.knight.x + 70

        knight_effect.y = knight_effect.knight.y
        knight_effect.start_time = get_time()

    def do(self, knight_effect:KnightEffect) -> AnimationState[KnightEffect] | None:

        if knight_effect.direction == 'left':
            knight_effect.x = knight_effect.knight.x - 70
        elif knight_effect.direction == 'right':
            knight_effect.x = knight_effect.knight.x + 70
        knight_effect.y = knight_effect.knight.y

        if get_time() - knight_effect.start_time > 0.5:
            return Delete()

        return None


    def exit(self,knight_effect):
        pass
