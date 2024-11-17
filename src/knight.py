
from entity import Entity
from pico2d import *
from input_manager import InputManager
from knight_effect import KnightEffect
import game_world
import game_framework
from src.animation import SpriteCollection
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
        self.hp = 5
        self.skill_point = 9
        self.hp_fill = load_image('../resource/ui/hp_fill.png')
        self.ground = y
        self.on_ground = True
        self.input_manager = InputManager()
        self.actionable = True
        self.font = load_font('../resource/font/ENCR10B.TTF', 16)

    def draw(self,collections: SpriteCollection):
        super().draw(collections.get(self.current_animation).draw(self.x, self.y, self.animation_time))
        self.font.draw(self.x - 10, self.y + 70, f'{self.skill_point:02d}', (255, 255, 0))
        for i in range(1, self.hp + 1):
            self.hp_fill.draw(65 * i, 650, 80, 100)

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

    def add_effect(self, direction,action):
        effect = KnightEffect(self,direction,action)
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
        knight.actionable = True

    def do(self, entity: Knight) -> AnimationState[Knight] | None:
        if entity.input_manager.jump: return Jump(self.direction)
        if entity.input_manager.slash and entity.input_manager.up:
            return Upslash(self.direction)
        if entity.input_manager.slash: return Slash(self.direction)
        if entity.input_manager.dash: return Dash(self.direction)
        if entity.input_manager.fireball_cast: return FireballCast(self.direction)
        if entity.input_manager.focus: return Focus(self.direction)
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
        if entity.input_manager.slash and entity.input_manager.up:
            return Upslash(self.direction)
        if entity.input_manager.slash: return Slash(self.direction)
        if entity.input_manager.dash and entity.actionable:
            return Dash(self.direction)
        if entity.input_manager.fireball_cast and entity.actionable and entity.skill_point >= 3:
            return FireballCast(self.direction)
        if entity.input_manager.focus and entity.actionable and entity.skill_point >= 3:
            return Focus(self.direction)
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


class Slash(AnimationState[Knight]):
    def __init__(self, direction: str):
        self.direction = direction

    def enter(self, knight):
        print('slash enter')
        if self.direction == 'right':
            knight.set_animation('knight_slash_right')
        elif self.direction == 'left':
            knight.set_animation('knight_slash_left')

        knight.add_effect(self.direction,'slash')
        knight.start_time = get_time()
        knight.actionable = False


    def exit(self, knight):
        pass

    def do(self, entity: Knight) -> AnimationState[Knight] | None:

        if get_time() - entity.start_time > 0.5:
            if not entity.on_ground:
                return OnAir(self.direction)
            if entity.input_manager.jump:
                return Jump(self.direction)

            if entity.input_manager.left and entity.input_manager.right:
                return Idle(self.direction)
            elif entity.input_manager.left:
                return Run('left')
            elif entity.input_manager.right:
                return Run('right')


            return Idle(self.direction)
        return None

class Upslash(AnimationState[Knight]):
    def __init__(self, direction: str):
        self.direction = direction

    def enter(self, knight):
        print('upslash enter')
        knight.set_animation('knight_upslash')
        knight.vx = 0

        knight.add_effect('up','slash')
        knight.start_time = get_time()
        knight.actionable = False

    def exit(self, knight):
        pass

    def do(self, entity: Knight) -> AnimationState[Knight] | None:

        if get_time() - entity.start_time > 0.5:
            if not entity.on_ground:
                return OnAir(self.direction)
            if entity.input_manager.jump:
                return Jump(self.direction)
            return Idle(self.direction)


        return None

class Downslash(AnimationState[Knight]):
    def __init__(self, direction: str):
        self.direction = direction

    def enter(self, knight):
        print('Downslash enter')
        knight.set_animation('knight_downslash')
        knight.vx = 0

        knight.add_effect('down','slash')
        knight.start_time = get_time()
        knight.actionable = False

    def exit(self, knight):
        pass

    def do(self, entity: Knight) -> AnimationState[Knight] | None:

        if get_time() - entity.start_time > 0.5:
            if not entity.on_ground:
                return OnAir(self.direction)
            if entity.input_manager.jump:
                return Jump(self.direction)

            return Idle(self.direction)
        return None


class Jump(AnimationState[Knight]):
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
        if get_time() - self.start_time > 0.5:
            return OnAir(self.direction)
        if entity.input_manager.slash and entity.input_manager.up and entity.actionable:
            return Upslash(self.direction)
        if entity.input_manager.slash and entity.input_manager.down and entity.actionable:
            return Downslash(self.direction)
        if entity.input_manager.slash and entity.actionable:
            return Slash(self.direction)
        if entity.input_manager.dash and entity.actionable:
            return Dash(self.direction)
        if entity.input_manager.fireball_cast and entity.actionable and entity.skill_point >= 3:
            return FireballCast(self.direction)
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
        if entity.input_manager.dash and entity.actionable:
            return Dash(self.direction)
        if entity.input_manager.slash and entity.input_manager.up and entity.actionable:
            return Upslash(self.direction)
        if entity.input_manager.slash and entity.input_manager.down and entity.actionable:
            return Downslash(self.direction)
        if entity.input_manager.slash and entity.actionable:
            return Slash(self.direction)
        if entity.input_manager.fireball_cast and entity.actionable and entity.skill_point >= 3:
            return FireballCast(self.direction)
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

class Dash(AnimationState[Knight]):
    def __init__(self, direction: str):
        self.direction = direction

    def enter(self, knight):
        if self.direction == 'right':
            knight.set_animation('knight_dash_right')
            knight.vx = 600
        elif self.direction == 'left':
            knight.set_animation('knight_dash_left')
            knight.vx = - 600

        knight.add_effect(self.direction, 'dash')
        knight.start_time = get_time()
        knight.actionable = False

    def do(self, knight: Knight) -> AnimationState[Knight] | None:
        if get_time() - knight.start_time > 0.5:
            if knight.on_ground:
                return Idle(self.direction)
            else:
                return OnAir(self.direction)

        return None
class FireballCast(AnimationState[Knight]):
    def __init__(self,direction:str):
        self.direction = direction

    def enter(self,knight):
        if self.direction == 'left':
            knight.set_animation('knight_fireball_cast_left')
        elif self.direction == 'right':
            knight.set_animation('knight_fireball_cast_right')

        knight.skill_point -= 3
        knight.add_effect(self.direction,'fireball_cast')
        knight.start_time = get_time()

    def do(self, knight:Knight) -> AnimationState[Knight] | None:
        if get_time() - knight.start_time > 0.5:
            if knight.on_ground:
                return Idle(self.direction)
            else:
                return OnAir(self.direction)
        pass

class Focus(AnimationState[Knight]):
    def __init__(self,direction):
        self.direction = direction

    def enter(self,knight):
        if self.direction == 'left':
            knight.set_animation('knight_focus_left')
        elif self.direction == 'right':
            knight.set_animation('knight_focus_right')

        knight.start_time = get_time()

    def do(self, knight:Knight) -> AnimationState[Knight] | None:
        if get_time() - knight.start_time > 1.4:
            knight.skill_point -= 3
            return Idle(self.direction)
        if knight.input_manager.left or knight.input_manager.right:
            return Idle(self.direction)
        if knight.input_manager.slash:
            return Slash(self.direction)
        if knight.input_manager.fireball_cast and knight.skill_point >= 3:
            return FireballCast(self.direction)

