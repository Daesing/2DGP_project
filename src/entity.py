from animation import SpriteAnimation, SpriteCollection


class Entity:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.current_animation = "knight_move_right"
        self.total_time = 0

    def draw_animation(self,collections: SpriteCollection):
        collections.get(self.current_animation).draw(self.x, self.y, self.total_time)


    def update(self, delta_time):
        self.total_time += delta_time




class Knight(Entity):
    def __init__(self,x,y):
        super().__init__()
        self.x = x
        self.y = y
        self.dir = 0




