from entity import Entity
from animation import SpriteCollection
from state_machine import AnimationState


class FalseKnight(Entity):

    def __init__(self,x,y):
        super().__init__(x, y, Idle('left'))
        self.x,y, = x,y


    def update(self):
        super().update()
        self.state_machine.update()

    def draw(self,collections: SpriteCollection):
        super().draw(collections.get(self.current_animation).draw(self.x, self.y, self.animation_time,420,270))

    def get_boundary(self, collections: SpriteCollection):
        value = collections.get(self.current_animation).get_size()
        width, height = value
        left = self.x - width / 2
        bottom = self.y - height / 2
        right = self.x + width / 2
        top = self.y + height / 2

        return left, bottom, right, top

    def handle_collision(self,group,other):
        if group == 'slash:false_knight':
            pass


class Idle(AnimationState[FalseKnight]):
    def __init__(self,direction):
        self.direction = direction

    def enter(self, false_knight):
        if self.direction == 'left':
            false_knight.set_animation('false_knight_idle_left')
        if self.direction == 'right':
            false_knight.set_animation('false_knight_idle_right')

    def do(self, false_knight:FalseKnight) -> AnimationState[FalseKnight] | None:

        return None





