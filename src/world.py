from src.animation import SpriteCollection
from src.entity import Entity
from pico2d import *

from src.knight import Knight


class World:

    def __init__(self, collections: SpriteCollection):
        self.entities = {}
        self.entity_id_counter = 0
        self.collections = collections
        self.running = True
        self.player_id = -1
        pass

    def update(self, delta_time: float):
        for entity_id, entity in self.entities.items():
            entity.update_time(delta_time)

        self.handle_events()

    def add_entity(self, entity: Entity):
        if isinstance(entity, Knight):
            self.player_id = self.entity_id_counter
        self.entities[self.entity_id_counter] = entity
        self.entity_id_counter += 1

    def render_entity(self):
        clear_canvas()
        for entity_id, entity in self.entities.items():
            entity.draw_animation(self.collections)
        update_canvas()

    def handle_events(self):
        events = get_events()
        for event in events:
            if event.type == SDL_QUIT:
                self.running = False
                return
            if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                self.running = False
                return
            if event.type in (SDL_KEYDOWN, SDL_KEYUP):
                self.entities[self.player_id].handle_event(event)  # input event

    def is_running(self) -> bool:
        return self.running
