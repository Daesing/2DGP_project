from typing import Any
import json
from pico2d import load_image, draw_rectangle


class SpriteAnimation:
    def __init__(self, image_path, frame_cnt, width_cnt, height_cnt):
        self.image = load_image(image_path)
        self.frame_cnt = frame_cnt
        self.width = self.image.w // width_cnt
        self.height = self.image.h // height_cnt
        self.frame_time = 30/60
        self.width_cnt = width_cnt
        self.height_cnt = height_cnt

    def draw(self, x, y, total_time, width = None, height = None):
        cycle_time = 3
        self.frame_time = cycle_time/self.frame_cnt

        current_frame = int((total_time // self.frame_time) % self.frame_cnt)
        sx = (current_frame % self.width_cnt) * self.width
        sy = (self.height_cnt - current_frame // self.width_cnt - 1) * self.height
        self.image.clip_draw(sx, sy, self.width, self.height, x, y, width, height)
        if width is None and height is None:
            draw_rectangle(x - self.width / 2, y - self.height / 2, x + self.width / 2, y + self.height / 2)
        else:
            draw_rectangle(x - width / 2, y - height / 2, x + width / 2, y + height / 2)

class SpriteCollection:
    def __init__(self):
        self.animations = {}
        self.initialized = False

    def initialize(self):
        with open('../resource/animations.json', 'r') as file:
            data = json.load(file)
            self.animations = {
                name: SpriteAnimation(
                    anim_data["path"],
                    anim_data["frames"],
                    anim_data["width"],
                    anim_data["height"]
                )
                for name, anim_data in data["animations"].items()
            }
        self.initialized = True

    def get(self,animation_name:str)-> SpriteAnimation:
        if not self.initialized:
            raise "not initialized"
        return self.animations[animation_name]

