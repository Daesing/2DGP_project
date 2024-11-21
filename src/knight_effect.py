from pico2d import load_image, get_time

from entity import Entity
from src.animation import SpriteCollection
from state_machine import Delete
from state_machine import AnimationState


class KnightEffect(Entity):
    start_time: float

    def __init__(self, knight,direction,action:str):
        self.knight = knight
        self.direction = direction
        self.action = action
        self.hit = True    #타 객체와의 중복 충돌을 막는 flag
        if action == 'slash':
            super().__init__(0, 0, SlashEffect())
        elif action == 'dash':
            super().__init__(0, 0, DashEffect())
        elif action == 'fireball_cast':
            super().__init__(0, 0, FireBall())


    def handle_collision(self,group,other):
        print('slash collision')
        if group == 'slash:false_knight' and self.hit:
            if self.knight.skill_point < 9:
                self.knight.skill_point += 1
            self.hit = False

    def update(self):
        super().update()
        self.state_machine.update()



class SlashEffect(AnimationState[KnightEffect]):
    def __init__(self):
        pass

    def enter(self, knight_effect):
        print('Slash effect enter')
        knight_effect.x = knight_effect.knight.x
        knight_effect.y = knight_effect.knight.y

        if knight_effect.direction == 'left':
            knight_effect.set_animation('knight_slash_effect',True)
            knight_effect.x = knight_effect.knight.x - 70
        elif knight_effect.direction == 'right':
            knight_effect.set_animation('knight_slash_effect')
            knight_effect.x = knight_effect.knight.x + 70
        elif knight_effect.direction == 'up':
            knight_effect.set_animation('knight_upslash_effect')
            knight_effect.y = knight_effect.knight.y + 70
        elif knight_effect.direction == 'down':
            knight_effect.set_animation('knight_downslash_effect')
            knight_effect.y = knight_effect.knight.y - 70


        knight_effect.start_time = get_time()

    def do(self, knight_effect:KnightEffect) -> AnimationState[KnightEffect] | None:
        knight_effect.x = knight_effect.knight.x
        knight_effect.y = knight_effect.knight.y

        if knight_effect.direction == 'left':
            knight_effect.x = knight_effect.knight.x - 70
        elif knight_effect.direction == 'right':
            knight_effect.x = knight_effect.knight.x + 70
        elif knight_effect.direction == 'up':
            knight_effect.y = knight_effect.knight.y + 70
        elif knight_effect.direction == 'down':
            knight_effect.y = knight_effect.knight.y - 70

        if get_time() - knight_effect.start_time > 0.4:
            return Delete()

        return None


    def exit(self,knight_effect):
        pass

class DashEffect(AnimationState[KnightEffect]):

    def __init__(self):
        pass

    def enter(self, knight_effect):
        knight_effect.y = knight_effect.knight.y

        if knight_effect.direction == 'right':
            knight_effect.set_animation('knight_dash_effect')
            knight_effect.x = knight_effect.knight.x - 100
        elif knight_effect.direction == 'left':
            knight_effect.set_animation('knight_dash_effect',True)
            knight_effect.x = knight_effect.knight.x + 100

        knight_effect.start_time = get_time()

    def do(self, knight_effect:KnightEffect) -> AnimationState[KnightEffect] | None:

        knight_effect.y = knight_effect.knight.y

        if knight_effect.direction == 'right':
            knight_effect.x = knight_effect.knight.x - 100
        elif knight_effect.direction == 'left':
            knight_effect.x = knight_effect.knight.x + 100

        if get_time() - knight_effect.start_time > 0.5:
            return Delete()


    def exit(self,knight_effect):
        pass

class FireBall(AnimationState[KnightEffect]):

    def __init__(self):
        pass

    def enter(self,knight_effect):
        knight_effect.y = knight_effect.knight.y

        if knight_effect.direction == 'right':
            knight_effect.set_animation('knight_fireball')
            knight_effect.x = knight_effect.knight.x + 10
        elif knight_effect.direction == 'left':
            knight_effect.set_animation('knight_fireball',True)
            knight_effect.x = knight_effect.knight.x - 10

        knight_effect.start_time = get_time()

    def do(self, knight_effect:KnightEffect) -> AnimationState[KnightEffect] | None:
        if knight_effect.direction == 'right':
            knight_effect.x += 4
        elif knight_effect.direction == 'left':
            knight_effect.x -= 4


        if get_time() - knight_effect.start_time > 0.5:
            return Delete()