from animation import SpriteCollection


class Entity:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.current_animation = "knight_idle_left"
        self.total_time = 0

    def draw_animation(self,collections: SpriteCollection):
        collections.get(self.current_animation).draw(self.x, self.y, self.total_time)


    def update_time(self, delta_time):
        self.total_time += delta_time
        self.update()

    def update(self):
        pass



